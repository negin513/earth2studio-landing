#!/usr/bin/env python3
"""Generate the Earth2Studio catalog registry from the source repository.

Parses the earth2studio source with `ast` + regex only — nothing is imported, so no
GPU, no CUDA, and none of the heavy optional extras (flash-attn, makani, graphcast…)
are needed. Emits JSON that the catalog pages, the hero counts, and CI all read from,
so the published inventory can never drift from the code.

Sources joined:
  1. ``earth2studio/{models/px,models/dx,models/da,data,perturbation,statistics,io}/__init__.py``
     -> the class inventory (import statements, NOT ``__all__``: dx's is stale)
  2. class docstring ``Badges`` blocks -> region / class / dataclass / product / year / VRAM
  3. ``docs/conf.py`` ``badges_definitions`` -> facet labels, tooltips, colors
  4. ``pyproject.toml`` ``[project.optional-dependencies]`` -> the pip extra per model
  5. ``load_default_package()`` bodies -> default checkpoint URI

Usage:
    python scripts/build_registry.py --source /path/to/earth2studio
    python scripts/build_registry.py --source /path/to/earth2studio --check   # CI drift guard
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

# Modules to inventory: (dotted path under earth2studio/, registry key)
MODULES: list[tuple[str, str]] = [
    ("models/px", "prognostic"),
    ("models/dx", "diagnostic"),
    ("models/da", "data_assimilation"),
    ("data", "data_sources"),
    ("perturbation", "perturbations"),
    ("statistics", "statistics"),
    ("io", "io_backends"),
]

# Protocols and plumbing: real classes, but not things a user *chooses between*.
# Kept in the registry with catalog=False so counts stay honest and the catalog
# pages stay a decision tool rather than an API dump.
NON_CATALOG = {
    # protocols
    "PrognosticModel", "DiagnosticModel", "DataSource", "ForecastSource",
    "Perturbation", "Metric", "Statistic", "IOBackend",
    # plumbing / synthetic / wrappers
    "DiagnosticWrapper", "Identity", "Persistence", "Random", "Random_FX",
    "Constant", "Constant_FX", "TimeWindow", "InferenceOutputSource",
    "DataArrayFile", "DataArrayDirectory", "DataArrayPathList", "DataSetFile",
    "RandomDataFrame",
    # module-level functions exported alongside classes
    "fetch_data", "fetch_dataframe", "prep_data_array", "datasource_to_file",
    "lat_weight",
}

BADGE_KEYS = ("region", "class", "dataclass", "product", "year", "gpu")


def parse_exports(init_path: Path) -> list[str]:
    """Public names from a module's ``__init__.py``.

    Uses the import statements rather than ``__all__``: ``models/dx/__init__.py``
    ships a stale ``__all__`` listing 10 of ~23 exported classes.
    """
    if not init_path.exists():
        return []
    tree = ast.parse(init_path.read_text())
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                if not name.startswith("_") and name != "*":
                    names.append(name)
    return sorted(set(names))


def parse_badges(docstring: str) -> dict[str, list[str]]:
    """Extract the trailing ``Badges`` block of a class docstring.

    Badge lines may wrap across multiple physical lines (e.g. ``dx/corrdiff.py``),
    so every line after the ``------`` underline is joined until a blank line.
    """
    if not docstring:
        return {}
    match = re.search(r"Badges\s*\n\s*-+\s*\n(.*?)(?:\n\s*\n|$)", docstring, re.S)
    if not match:
        return {}
    tokens = match.group(1).split()
    badges: dict[str, list[str]] = {}
    for token in tokens:
        if ":" not in token:
            continue
        key, _, value = token.partition(":")
        if key in BADGE_KEYS and value:
            badges.setdefault(key, []).append(value)
    return badges


REF_HOSTS = ("arxiv.org", "huggingface.co", "ngc.nvidia.com", "github.com", "doi.org")


def parse_references(docstring: str) -> list[str]:
    """Reference URLs from the ``Note`` docstring section (papers, model cards)."""
    if not docstring:
        return []
    urls = re.findall(r"https?://[^\s<>\"')]+", docstring)
    seen: list[str] = []
    for url in urls:
        url = url.rstrip(".,)")
        if any(host in url for host in REF_HOSTS) and url not in seen:
            seen.append(url)
    return seen


def parse_warning(docstring: str) -> str | None:
    """The ``Warning`` docstring section — usually licensing or download size."""
    if not docstring:
        return None
    match = re.search(r"Warning\s*\n\s*-+\s*\n(.*?)(?:\n\s*\n\s*\w+\s*\n\s*-+|\Z)", docstring, re.S)
    if not match:
        return None
    return " ".join(match.group(1).split()) or None


# Phrasing is consistent enough across data-source docstrings to structure:
#   "0.25 degree lat lon grid", "3km", "at 6-hour intervals", "Temporal resolution is 1 hour"
RE_SPATIAL = re.compile(r"(\d+(?:\.\d+)?)\s*(?:degree|deg|km)\b", re.I)
RE_TEMPORAL = re.compile(r"(?:at\s+)?(\d+)[- ]hour(?:ly)?(?:\s+intervals)?|temporal resolution is (\d+)\s*hour", re.I)


def parse_grid(docstring: str) -> dict[str, str]:
    """Best-effort spatial/temporal resolution from data-source prose."""
    out: dict[str, str] = {}
    if not docstring:
        return out
    head = " ".join(docstring.split("\n\n")[0].split())
    spatial = RE_SPATIAL.search(head)
    if spatial:
        unit = "km" if "km" in spatial.group(0).lower() else "\u00b0"
        out["resolution"] = f"{spatial.group(1)}{unit}"
    temporal = RE_TEMPORAL.search(head)
    if temporal:
        hours = temporal.group(1) or temporal.group(2)
        if hours:
            out["cadence"] = f"{hours}h"
    return out


LICENSE_SENTENCE = "We encourage users to familiarize themselves with the license restrictions"
UNIT_HOURS = {"h": 1.0, "m": 1 / 60, "s": 1 / 3600, "D": 24.0, "W": 168.0}


def _coord_dicts(class_node: ast.ClassDef) -> list[ast.Dict]:
    """CoordSystem dict literals inside the class (those with a 'variable' or
    'lead_time' key) — these carry the grid, variables, and time step."""
    found = []
    for node in ast.walk(class_node):
        if not isinstance(node, ast.Dict):
            continue
        keys = {k.value for k in node.keys if isinstance(k, ast.Constant)}
        if "variable" in keys or "lead_time" in keys:
            found.append(node)
    return found


def _dict_value(node: ast.Dict, key: str) -> ast.AST | None:
    for k, v in zip(node.keys, node.values):
        if isinstance(k, ast.Constant) and k.value == key:
            return v
    return None


def _timedeltas(node: ast.AST) -> list[float]:
    """Every np.timedelta64(value, unit) under a node, in hours."""
    out = []
    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call):
            continue
        fn = sub.func
        name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
        if name != "timedelta64" or len(sub.args) < 2:
            continue
        try:
            value = ast.literal_eval(sub.args[0])
            unit = ast.literal_eval(sub.args[1])
        except (ValueError, SyntaxError):
            continue
        if unit in UNIT_HOURS:
            out.append(float(value) * UNIT_HOURS[unit])
    return out


def _override_step(class_node: ast.ClassDef) -> float | None:
    """Time step set by assignment rather than in a coord literal.

    Pangu24/Pangu6/Pangu3 inherit PanguBase's 6h coord dict and then reassign
    ``self._output_coords["lead_time"]`` in ``__init__`` — without this, a
    subclass would inherit the base's step and be reported wrongly.
    """
    steps: list[float] = []
    for node in ast.walk(class_node):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Subscript):
                continue
            key = target.slice
            if not (isinstance(key, ast.Constant) and key.value == "lead_time"):
                continue
            value = target.value
            attr = getattr(value, "attr", "")
            if "output_coords" not in attr:
                continue
            steps.extend(d for d in _timedeltas(node.value) if d > 0)
    return min(steps) if steps else None


def parse_coords(class_node: ast.ClassDef) -> dict[str, Any]:
    """Time step, history requirement, and grid shape from the coord systems.

    Deliberately conservative: only literal np.linspace/timedelta64 calls are read.
    Anything computed at load time (AIFS resolves its variables from checkpoint
    metadata) is left absent rather than guessed.
    """
    out: dict[str, Any] = {}
    steps: list[float] = []
    history: list[float] = []

    for coord in _coord_dicts(class_node):
        lead = _dict_value(coord, "lead_time")
        if lead is not None:
            deltas = _timedeltas(lead)
            positive = [d for d in deltas if d > 0]
            negative = [d for d in deltas if d < 0]
            steps.extend(positive)
            history.extend(negative)

        # Grid: np.linspace(90, -90, N) on lat / lon
        if "shape" not in out:
            lat, lon = _dict_value(coord, "lat"), _dict_value(coord, "lon")
            dims = [_linspace_n(lat), _linspace_n(lon)]
            if all(dims):
                out["shape"] = f"{dims[0]}\u00d7{dims[1]}"
                # 0.25deg on a 721-row grid includes both poles; 720 excludes the south
                out["degrees"] = round(360 / dims[1], 4)

    if steps:
        out["time_step_h"] = min(steps)
    if history:
        out["history_h"] = abs(min(history))
    return out


def _linspace_n(node: ast.AST | None) -> int | None:
    """The point count from an np.linspace(...) / np.arange-style coordinate."""
    if node is None:
        return None
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            fn = sub.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
            if name == "linspace" and len(sub.args) >= 3:
                try:
                    return int(ast.literal_eval(sub.args[2]))
                except (ValueError, SyntaxError, TypeError):
                    return None
    return None


def parse_default_package(class_node: ast.ClassDef) -> str | None:
    """Default checkpoint URI from ``load_default_package()``.

    Returns None for abstract bases that raise NotImplementedError (e.g. ``CorrDiff``)
    and for classes that fetch several packages (only the first URI is reported).
    """
    for node in class_node.body:
        if not isinstance(node, ast.FunctionDef) or node.name != "load_default_package":
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                if re.match(r"^(hf|ngc|s3|https?)://", sub.value):
                    return sub.value
    return None


def _inherited_coords(
    class_node: ast.ClassDef, by_name: dict[str, ast.ClassDef]
) -> dict[str, Any]:
    """Walk same-file base classes for coords.

    Eight catalog classes define no coords of their own (Pangu24/6/3 -> PanguBase,
    StormScopeGOES/MRMS -> StormScopeBase, DLESyMLatLon -> DLESyM, ...).
    """
    seen: set[str] = set()
    queue = [b.id for b in class_node.bases if isinstance(b, ast.Name)]
    while queue:
        name = queue.pop(0)
        if name in seen or name not in by_name:
            continue
        seen.add(name)
        base = by_name[name]
        coords = parse_coords(base)
        if coords:
            return coords
        queue.extend(b.id for b in base.bases if isinstance(b, ast.Name))
    return {}


def _resolve_coords(
    class_node: ast.ClassDef, by_name: dict[str, ast.ClassDef]
) -> dict[str, Any]:
    """Class coords, falling back to same-file bases, with subclass step overrides."""
    coords = parse_coords(class_node) or _inherited_coords(class_node, by_name)
    override = _override_step(class_node)
    if override is not None:
        coords = dict(coords)
        coords["time_step_h"] = override
    return coords


def scan_module(source: Path, module: str) -> dict[str, dict[str, Any]]:
    """Class name -> metadata for every class defined under ``earth2studio/<module>/``."""
    found: dict[str, dict[str, Any]] = {}
    for py in sorted((source / "earth2studio" / module).glob("*.py")):
        if py.name == "__init__.py":
            continue
        try:
            tree = ast.parse(py.read_text())
        except SyntaxError:
            continue
        by_name = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            doc = ast.get_docstring(node) or ""
            summary = " ".join(doc.split("\n\n")[0].split()) if doc else ""
            found[node.name] = {
                "summary": summary,
                "badges": parse_badges(doc),
                "checkpoint": parse_default_package(node),
                "references": parse_references(doc),
                "warning": parse_warning(doc),
                "grid": parse_grid(doc),
                "coords": _resolve_coords(node, by_name),
                "source_file": f"earth2studio/{module}/{py.name}",
            }
    return found


def parse_extras(source: Path) -> dict[str, list[str]]:
    """``[project.optional-dependencies]`` names -> their requirement lists."""
    text = (source / "pyproject.toml").read_text()
    block = re.search(
        r"\[project\.optional-dependencies\](.*?)(?=\n\[[a-z])", text, re.S
    )
    if not block:
        return {}
    extras: dict[str, list[str]] = {}
    for name, body in re.findall(r"^([a-z0-9_-]+)\s*=\s*\[(.*?)\]", block.group(1), re.S | re.M):
        reqs = [r.strip().strip('"\'') for r in body.split(",") if r.strip()]
        extras[name] = [r for r in reqs if r]
    return extras


def match_extra(class_name: str, extras: dict[str, list[str]]) -> str | None:
    """Best-guess pip extra for a model class (``FCN3`` -> ``fcn3``)."""
    lowered = class_name.lower()
    if lowered in extras:
        return lowered
    hyphenated = re.sub(r"(?<!^)(?=[A-Z])", "-", class_name).lower()
    if hyphenated in extras:
        return hyphenated
    for candidate in sorted(extras, key=len, reverse=True):
        if len(candidate) >= 4 and candidate.replace("-", "") in lowered:
            return candidate
    return None


def parse_facets(source: Path) -> dict[str, Any]:
    """``badges_definitions`` from docs/conf.py — the label/tooltip/color taxonomy."""
    text = (source / "docs" / "conf.py").read_text()
    match = re.search(r"^badges_definitions\s*=\s*(\{.*?^\})", text, re.S | re.M)
    if not match:
        return {}
    try:
        raw = ast.literal_eval(match.group(1))
    except (ValueError, SyntaxError):
        return {}
    facets: dict[str, dict[str, Any]] = {}
    for token, meta in raw.items():
        if ":" not in token:
            continue
        group, _, value = token.partition(":")
        meta = {k: v for k, v in meta.items() if k != "icon"}  # icons are raw HTML
        facets.setdefault(group, {})[value] = meta
    return facets


def parse_vocabulary(source: Path) -> dict[str, str]:
    """``E2STUDIO_VOCAB`` — the canonical variable glossary (id -> description)."""
    path = source / "earth2studio" / "lexicon" / "base.py"
    if not path.exists():
        return {}
    for node in ast.parse(path.read_text()).body:
        target = None
        if isinstance(node, ast.Assign):
            target = getattr(node.targets[0], "id", None)
        elif isinstance(node, ast.AnnAssign):
            target = getattr(node.target, "id", None)
        if target == "E2STUDIO_VOCAB":
            try:
                return ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                return {}
    return {}


def parse_source_variables(source: Path) -> dict[str, int]:
    """Lexicon class -> number of variables it maps.

    24 of 54 lexicons build ``VOCAB`` dynamically (comprehensions/loops); those are
    skipped rather than guessed at.
    """
    counts: dict[str, int] = {}
    for py in sorted((source / "earth2studio" / "lexicon").glob("*.py")):
        if py.name in {"__init__.py", "base.py"}:
            continue
        try:
            tree = ast.parse(py.read_text())
        except SyntaxError:
            continue
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            for sub in node.body:
                target = None
                if isinstance(sub, ast.AnnAssign):
                    target = getattr(sub.target, "id", None)
                elif isinstance(sub, ast.Assign):
                    target = getattr(sub.targets[0], "id", None)
                if target != "VOCAB":
                    continue
                try:
                    counts[node.name] = len(ast.literal_eval(sub.value))
                except (ValueError, SyntaxError):
                    pass  # dynamically built — not statically countable
    return counts


def build(source: Path) -> dict[str, Any]:
    extras = parse_extras(source)
    registry: dict[str, Any] = {
        "_meta": {
            "source": str(source),
            "generator": "scripts/build_registry.py",
            "note": "Generated file — do not edit by hand. Run the generator instead.",
        },
        "facets": parse_facets(source),
        "vocabulary": parse_vocabulary(source),
    }
    variables = parse_source_variables(source)

    for module, key in MODULES:
        exported = parse_exports(source / "earth2studio" / module / "__init__.py")
        scanned = scan_module(source, module)
        entries = []
        for name in exported:
            meta = scanned.get(name, {})
            catalog = name not in NON_CATALOG and not name.startswith("Derived")
            entry: dict[str, Any] = {
                "name": name,
                "catalog": catalog,
                "summary": meta.get("summary", ""),
                "badges": meta.get("badges", {}),
                "source_file": meta.get("source_file"),
            }
            if meta.get("checkpoint"):
                entry["checkpoint"] = meta["checkpoint"]
            if meta.get("references"):
                entry["references"] = meta["references"]
            if meta.get("warning"):
                entry["warning"] = meta["warning"]
                if meta["warning"].startswith(LICENSE_SENTENCE):
                    entry["license_restricted"] = True
            if meta.get("grid"):
                entry["grid"] = meta["grid"]
            if meta.get("coords"):
                entry["coords"] = meta["coords"]
            if key == "data_sources":
                nvars = variables.get(f"{name}Lexicon")
                if nvars:
                    entry["variables"] = nvars
            if key in {"prognostic", "diagnostic", "data_assimilation"}:
                entry["extra"] = match_extra(name, extras)
            entries.append(entry)
        registry[key] = entries

    registry["counts"] = {
        key: {
            "total": len(registry[key]),
            "catalog": sum(1 for e in registry[key] if e["catalog"]),
            "badged": sum(1 for e in registry[key] if e["badges"]),
        }
        for _, key in MODULES
    }
    models = ("prognostic", "diagnostic", "data_assimilation")
    registry["counts"]["models_total"] = sum(
        registry["counts"][k]["catalog"] for k in models
    )
    registry["counts"]["vocabulary"] = len(registry["vocabulary"])
    return registry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="earth2studio checkout")
    parser.add_argument("--out", type=Path, default=Path("docs/data/registry.json"))
    parser.add_argument("--check", action="store_true", help="fail if output is stale")
    args = parser.parse_args()

    if not (args.source / "earth2studio").is_dir():
        print(f"error: {args.source} is not an earth2studio checkout", file=sys.stderr)
        return 2

    registry = build(args.source)
    registry["_meta"].pop("source")  # keep output machine-independent
    rendered = json.dumps(registry, indent=2, sort_keys=True) + "\n"

    if args.check:
        if not args.out.exists() or args.out.read_text() != rendered:
            print(
                f"error: {args.out} is stale — rerun scripts/build_registry.py",
                file=sys.stderr,
            )
            return 1
        print(f"{args.out} is up to date")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(rendered)

    counts = registry["counts"]
    print(f"wrote {args.out}")
    for _, key in MODULES:
        c = counts[key]
        print(f"  {key:18} {c['catalog']:3} catalog / {c['total']:3} exported / {c['badged']:3} badged")
    print(f"  {'models_total':18} {counts['models_total']:3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
