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
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            doc = ast.get_docstring(node) or ""
            summary = " ".join(doc.split("\n\n")[0].split()) if doc else ""
            found[node.name] = {
                "summary": summary,
                "badges": parse_badges(doc),
                "checkpoint": parse_default_package(node),
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


def build(source: Path) -> dict[str, Any]:
    extras = parse_extras(source)
    registry: dict[str, Any] = {
        "_meta": {
            "source": str(source),
            "generator": "scripts/build_registry.py",
            "note": "Generated file — do not edit by hand. Run the generator instead.",
        },
        "facets": parse_facets(source),
    }

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
