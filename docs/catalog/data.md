# Data source catalog

Every data source Earth2Studio can stream from — reanalysis, operational forecasts,
satellite and in-situ observations — all behind one interface.

!!! info "Generated from source"
    This page is generated from the Earth2Studio source. It cannot drift from the code.

<div class="e2s-catalog" data-catalog="data">
  <input class="e2s-search" type="search" placeholder="Search sources, products, descriptions…" aria-label="Search data sources">
  <div class="e2s-facets"></div>
  <p class="e2s-count-line"><span class="e2s-shown"></span> shown · <a href="#" class="e2s-reset">reset filters</a></p>

{% set groups = [
  ('reanalysis', 'Reanalysis', 'Historical, analysis-ready atmospheric state.'),
  ('analysis', 'Analysis', 'Best-estimate current state — the usual forecast initial conditions.'),
  ('simulation', 'Forecast / simulation', 'Model forecast output and reforecast archives.'),
  ('observation', 'Observations', 'Direct measurements: satellite instruments, stations, events.')
] %}

{% for key, title, blurb in groups %}
## {{ title }}

{{ blurb }}

<div class="e2s-table">
<table class="e2s-rows">
<thead><tr><th>Source</th><th>Coverage</th><th>Products</th><th>Description</th></tr></thead>
<tbody>
{%- for d in entries('data_sources') if key in (d.badges.dataclass or []) %}
<tr data-href="https://nvidia.github.io/earth2studio/modules/datasources_analysis.html"
    data-region="{{ d.badges.region | join(' ') }}" data-dataclass="{{ d.badges.dataclass | join(' ') }}"
    data-product="{{ d.badges['product'] | join(' ') }}">
<td><code>{{ d.name }}</code></td>
<td>{{ d.badges.region | join(', ') | upper if d.badges.region else '—' }}</td>
<td>{{ d.badges['product'] | join(', ') if d.badges['product'] else '—' }}</td>
<td>{{ d.summary | truncate(110) }}</td>
</tr>
{%- endfor %}
</tbody>
</table>
</div>
{% endfor %}

</div>

Sources without a data class badge (utilities, synthetic sources, and file readers) are
documented in the API reference. Click any row to open the API docs.

[Full API reference :octicons-arrow-right-24:](https://nvidia.github.io/earth2studio/modules/datasources_analysis.html){ .md-button }
