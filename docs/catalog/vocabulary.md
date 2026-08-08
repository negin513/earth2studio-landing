# Variable glossary

Earth2Studio uses one canonical variable ID across every model and data source, so a
pipeline can swap either without renaming anything. This is the full vocabulary —
**{{ n('vocabulary') }} variables**.

!!! info "Generated from source"
    Generated from `E2STUDIO_VOCAB` in `earth2studio/lexicon/base.py`. It cannot drift
    from the code.

## Naming conventions

| Pattern | Meaning | Example |
| --- | --- | --- |
| `<var>` | Surface or single-level field | `msl` — mean sea level pressure |
| `<var><height>m` | Field at a height above ground | `u10m` — u-wind at 10 m |
| `<var><level>` | Field on a pressure level, in hPa | `z500` — geopotential at 500 hPa |
| `<var><hours>` | Accumulated over the preceding window | `tp06` — precipitation over 6 h |

<div class="e2s-catalog" data-catalog="vocabulary">
  <input class="e2s-search" type="search" placeholder="Search variables — try “wind”, “500”, “precip”…" aria-label="Search variables">
  <p class="e2s-count-line"><span class="e2s-shown"></span> shown · <a href="#" class="e2s-reset">reset</a></p>

<div class="e2s-table">
<table class="e2s-rows">
<thead><tr><th>Variable</th><th>Description</th></tr></thead>
<tbody>
{%- for name, desc in registry.vocabulary.items() %}
<tr><td><code>{{ name }}</code></td><td>{{ desc }}</td></tr>
{%- endfor %}
</tbody>
</table>
</div>

</div>

Each data source maps these IDs onto its own native names through a lexicon — see the
[data source catalog](data.md) for how many variables each source provides.

[Lexicon user guide :octicons-arrow-right-24:](https://nvidia.github.io/earth2studio/userguide/advanced/lexicon.html){ .md-button }
