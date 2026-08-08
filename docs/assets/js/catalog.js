/* Faceted, searchable catalog tables.
 *
 * Builds filter chips from the data-* attributes the registry template emits on each
 * row, then filters client-side. No dependencies, no backend. Rows are clickable and
 * keyboard-navigable; the anchor inside the first cell stays the accessible target.
 */
(function () {
  "use strict";

  var GROUPS = [
    { key: "region", label: "Coverage" },
    { key: "class", label: "Type" },
    { key: "dataclass", label: "Data class" },
    { key: "product", label: "Product" },
    { key: "gpu", label: "Rec. VRAM" },
  ];

  var LABELS = {
    mrf: "Medium range", nwc: "Nowcasting", ds: "Downscaling",
    s2s: "Subseasonal", cm: "Climate", da: "Data assimilation",
    global: "Global", na: "N. America", eu: "Europe", as: "Asia",
    au: "Oceania", af: "Africa", sa: "S. America",
    reanalysis: "Reanalysis", analysis: "Analysis",
    simulation: "Forecast", observation: "Observations",
  };

  function pretty(group, value) {
    if (LABELS[value]) return LABELS[value];
    if (group === "gpu") return value.toUpperCase();
    return value.charAt(0).toUpperCase() + value.slice(1);
  }

  function initCatalog(root) {
    if (root.dataset.e2sInit) return;
    root.dataset.e2sInit = "1";

    var rows = Array.prototype.slice.call(root.querySelectorAll("table.e2s-rows tbody tr"));
    if (!rows.length) return;

    var facetBox = root.querySelector(".e2s-facets");
    var search = root.querySelector(".e2s-search");
    var shown = root.querySelector(".e2s-shown");
    var reset = root.querySelector(".e2s-reset");
    var active = Object.create(null); // group -> Set of selected values

    // ── Row click-through ────────────────────────────────────────────────
    rows.forEach(function (row) {
      var href = row.dataset.href;
      if (!href) return;
      row.classList.add("e2s-clickable");
      row.tabIndex = 0;
      row.setAttribute("role", "link");
      row.addEventListener("click", function (e) {
        if (e.target.closest("a")) return; // let real links win
        window.open(href, "_blank", "noopener");
      });
      row.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          window.open(href, "_blank", "noopener");
        }
      });
    });

    // ── Build chips from the values actually present ─────────────────────
    GROUPS.forEach(function (group) {
      var values = Object.create(null);
      rows.forEach(function (row) {
        (row.dataset[group.key] || "").split(/\s+/).forEach(function (v) {
          if (v) values[v] = (values[v] || 0) + 1;
        });
      });
      var keys = Object.keys(values).sort();
      if (!keys.length) return;

      var wrap = document.createElement("div");
      wrap.className = "e2s-facet-group";
      wrap.innerHTML = '<span class="e2s-facet-label">' + group.label + "</span>";

      keys.forEach(function (value) {
        var chip = document.createElement("button");
        chip.type = "button";
        chip.className = "e2s-chip";
        chip.dataset.group = group.key;
        chip.dataset.value = value;
        chip.setAttribute("aria-pressed", "false");
        chip.innerHTML = pretty(group.key, value) +
          ' <span class="e2s-chip__n">' + values[value] + "</span>";
        chip.addEventListener("click", function () {
          var set = active[group.key] || (active[group.key] = new Set());
          if (set.has(value)) {
            set.delete(value);
            chip.setAttribute("aria-pressed", "false");
          } else {
            set.add(value);
            chip.setAttribute("aria-pressed", "true");
          }
          apply();
        });
        wrap.appendChild(chip);
      });
      facetBox.appendChild(wrap);
    });

    // ── Filtering ────────────────────────────────────────────────────────
    function apply() {
      var query = (search && search.value || "").trim().toLowerCase();
      var visible = 0;

      rows.forEach(function (row) {
        // OR within a group, AND across groups — mirrors the Sphinx badge-filter.
        var pass = Object.keys(active).every(function (group) {
          var set = active[group];
          if (!set || !set.size) return true;
          var have = (row.dataset[group] || "").split(/\s+/);
          return have.some(function (v) { return set.has(v); });
        });
        if (pass && query) {
          pass = row.textContent.toLowerCase().indexOf(query) !== -1;
        }
        row.hidden = !pass;
        if (pass) visible++;
      });

      if (shown) shown.textContent = visible + " of " + rows.length;

      // Hide a section whose table has no visible rows left.
      root.querySelectorAll("table.e2s-rows").forEach(function (table) {
        var any = table.querySelector("tbody tr:not([hidden])");
        var section = table.closest(".e2s-table");
        if (section) section.hidden = !any;
      });
    }

    if (search) search.addEventListener("input", apply);
    if (reset) {
      reset.addEventListener("click", function (e) {
        e.preventDefault();
        active = Object.create(null);
        if (search) search.value = "";
        root.querySelectorAll(".e2s-chip[aria-pressed='true']").forEach(function (c) {
          c.setAttribute("aria-pressed", "false");
        });
        apply();
      });
    }

    apply();
  }

  function init() {
    document.querySelectorAll(".e2s-catalog").forEach(initCatalog);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(init); // Material instant navigation
  }
})();
