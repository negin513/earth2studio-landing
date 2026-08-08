# Model catalog

Every AI model Earth2Studio can run, with the facts you need to choose one:
what it forecasts, where, at what recommended GPU memory, and how to install it.

!!! info "Generated from source"
    This page is generated from the Earth2Studio source — model docstrings,
    `pyproject.toml` extras, and checkpoint URIs. It cannot drift from the code.

!!! warning "Model licenses"
    Earth2Studio is an interface to third-party models, checkpoints, and datasets.
    Licenses for these assets are owned by their providers — ensure you have the
    rights to download, use, and (if applicable) redistribute each model and dataset.
    Apache-2.0 covers the Earth2Studio code only.

<div class="e2s-catalog" data-catalog="models">
  <input class="e2s-search" type="search" placeholder="Search models, products, checkpoints…" aria-label="Search models">
  <div class="e2s-facets"></div>
  <p class="e2s-count-line"><span class="e2s-shown"></span> shown · <a href="#" class="e2s-reset">reset filters</a></p>

## Prognostic models ({{ n('prognostic') }})

Prognostic models perform time integration — given the atmospheric state now, they
predict the next state and roll forward to build a forecast.

<div class="e2s-table">
<table class="e2s-rows">
<thead><tr><th>Model</th><th>Coverage</th><th>Type</th><th>Products</th><th>Rec. VRAM</th><th>Install</th><th>Checkpoint</th><th>Refs</th></tr></thead>
<tbody>
{%- for m in entries('prognostic') %}
<tr data-href="https://nvidia.github.io/earth2studio/modules/generated/models/px/earth2studio.models.px.{{ m.name }}.html"
    data-region="{{ m.badges.region | join(' ') }}" data-class="{{ m.badges['class'] | join(' ') }}"
    data-product="{{ m.badges['product'] | join(' ') }}" data-gpu="{{ m.badges.gpu | join(' ') }}"
    data-year="{{ m.badges.year | join(' ') }}">
<td><code>{{ m.name }}</code></td>
<td>{{ m.badges.region | join(', ') | upper if m.badges.region else '—' }}</td>
<td>{{ m.badges['class'] | join(', ') | upper if m.badges['class'] else '—' }}</td>
<td>{{ m.badges['product'] | join(', ') if m.badges['product'] else '—' }}</td>
<td>{{ m.badges.gpu | join(', ') | upper if m.badges.gpu else '—' }}</td>
<td>{% if m.extra %}<code>[{{ m.extra }}]</code>{% else %}—{% endif %}</td>
<td>{% if m.checkpoint %}<code>{{ m.checkpoint.split('@')[0] }}</code>{% else %}—{% endif %}</td>
<td class="e2s-refs">{% for r in m.references %}{% if 'arxiv' in r %}<a href="{{ r }}" title="Paper">📄</a>{% elif 'huggingface' in r %}<a href="{{ r }}" title="Hugging Face">🤗</a>{% elif 'ngc' in r %}<a href="{{ r }}" title="NGC">NGC</a>{% elif 'github' in r %}<a href="{{ r }}" title="GitHub">⌥</a>{% endif %}{% endfor %}{% if m.warning %}<span class="e2s-warn" title="{{ m.warning | truncate(220) | e }}">⚠</span>{% endif %}</td>
</tr>
{%- endfor %}
</tbody>
</table>
</div>

## Diagnostic models ({{ n('diagnostic') }})

Diagnostic models derive new quantities from existing fields — precipitation,
downscaling to higher resolution, cyclone tracking, and other decision-ready variables.

<div class="e2s-table">
<table class="e2s-rows">
<thead><tr><th>Model</th><th>Coverage</th><th>Type</th><th>Products</th><th>Rec. VRAM</th><th>Install</th><th>Refs</th></tr></thead>
<tbody>
{%- for m in entries('diagnostic') %}
<tr data-href="https://nvidia.github.io/earth2studio/modules/generated/models/dx/earth2studio.models.dx.{{ m.name }}.html"
    data-region="{{ m.badges.region | join(' ') }}" data-class="{{ m.badges['class'] | join(' ') }}"
    data-product="{{ m.badges['product'] | join(' ') }}" data-gpu="{{ m.badges.gpu | join(' ') }}"
    data-year="{{ m.badges.year | join(' ') }}">
<td><code>{{ m.name }}</code></td>
<td>{{ m.badges.region | join(', ') | upper if m.badges.region else '—' }}</td>
<td>{{ m.badges['class'] | join(', ') | upper if m.badges['class'] else '—' }}</td>
<td>{{ m.badges['product'] | join(', ') if m.badges['product'] else '—' }}</td>
<td>{{ m.badges.gpu | join(', ') | upper if m.badges.gpu else '—' }}</td>
<td>{% if m.extra %}<code>[{{ m.extra }}]</code>{% else %}—{% endif %}</td>
<td class="e2s-refs">{% for r in m.references %}{% if 'arxiv' in r %}<a href="{{ r }}" title="Paper">📄</a>{% elif 'huggingface' in r %}<a href="{{ r }}" title="Hugging Face">🤗</a>{% elif 'ngc' in r %}<a href="{{ r }}" title="NGC">NGC</a>{% elif 'github' in r %}<a href="{{ r }}" title="GitHub">⌥</a>{% endif %}{% endfor %}{% if m.warning %}<span class="e2s-warn" title="{{ m.warning | truncate(220) | e }}">⚠</span>{% endif %}</td>
</tr>
{%- endfor %}
</tbody>
</table>
</div>

## Data assimilation models ({{ n('data_assimilation') }})

<div class="e2s-table">
<table class="e2s-rows">
<thead><tr><th>Model</th><th>Coverage</th><th>Install</th><th>Description</th></tr></thead>
<tbody>
{%- for m in entries('data_assimilation') %}
<tr data-href="https://nvidia.github.io/earth2studio/modules/models_da.html"
    data-region="{{ m.badges.region | join(' ') }}" data-class="{{ m.badges['class'] | join(' ') }}"
    data-product="{{ m.badges['product'] | join(' ') }}" data-gpu="{{ m.badges.gpu | join(' ') }}"
    data-year="{{ m.badges.year | join(' ') }}">
<td><code>{{ m.name }}</code></td>
<td>{{ m.badges.region | join(', ') | upper if m.badges.region else '—' }}</td>
<td>{% if m.extra %}<code>[{{ m.extra }}]</code>{% else %}—{% endif %}</td>
<td>{{ m.summary | truncate(90) }}</td>
</tr>
{%- endfor %}
</tbody>
</table>
</div>

</div>

**Legend** — *Type*: MRF medium-range forecast · NWC nowcasting · DS downscaling ·
S2S subseasonal-to-seasonal · CM climate · DA data assimilation.
*Install*: the pip extra, e.g. `pip install earth2studio[fcn3]`.
*Refs*: 📄 paper · 🤗 Hugging Face · NGC catalog · ⌥ GitHub · ⚠ licensing note (hover).
Click any row to open its API reference.

[Full API reference :octicons-arrow-right-24:](https://nvidia.github.io/earth2studio/modules/models_px.html){ .md-button }
