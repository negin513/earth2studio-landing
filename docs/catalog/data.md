# Data source catalog

Every data source Earth2Studio can stream from — reanalysis, operational forecasts,
satellite and in-situ observations — all behind one interface.

!!! info "Generated from source"
    This page is generated from the Earth2Studio source. It cannot drift from the code.

{% set groups = [
  ('reanalysis', 'Reanalysis', 'Historical, analysis-ready atmospheric state.'),
  ('analysis', 'Analysis', 'Best-estimate current state — the usual forecast initial conditions.'),
  ('simulation', 'Forecast / simulation', 'Model forecast output and reforecast archives.'),
  ('observation', 'Observations', 'Direct measurements: satellite instruments, stations, events.')
] %}

{% for key, title, blurb in groups %}
## {{ title }}

{{ blurb }}

<div class="e2s-table" markdown>

| Source | Coverage | Products | Description |
| --- | --- | --- | --- |
{% for d in entries('data_sources') if key in (d.badges.dataclass or []) -%}
| `{{ d.name }}` | {{ d.badges.region | join(', ') | upper if d.badges.region else '—' }} | {{ d.badges['product'] | join(', ') if d.badges['product'] else '—' }} | {{ d.summary | truncate(110) }} |
{% endfor %}

</div>
{% endfor %}

## Other sources

Sources without a data class badge (utilities, synthetic sources, and file readers) are
documented in the API reference.

---

[Full API reference :octicons-arrow-right-24:](https://nvidia.github.io/earth2studio/modules/datasources_analysis.html){ .md-button }
