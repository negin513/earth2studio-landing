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

<div class="e2s-facets" data-target="px" markdown>
Filter: <span class="e2s-facet-chips"></span>
</div>

## Prognostic models ({{ n('prognostic') }})

Prognostic models perform time integration — given the atmospheric state now, they
predict the next state and roll forward to build a forecast.

<div class="e2s-table" markdown>

| Model | Coverage | Type | Products | Rec. VRAM | Install | Checkpoint |
| --- | --- | --- | --- | --- | --- | --- |
{% for m in entries('prognostic') -%}
| [`{{ m.name }}`](https://nvidia.github.io/earth2studio/modules/generated/models/px/earth2studio.models.px.{{ m.name }}.html) | {{ m.badges.region | join(', ') | upper if m.badges.region else '—' }} | {{ m.badges['class'] | join(', ') | upper if m.badges['class'] else '—' }} | {{ m.badges['product'] | join(', ') if m.badges['product'] else '—' }} | {{ m.badges.gpu | join(', ') | upper if m.badges.gpu else '—' }} | {% if m.extra %}`[{{ m.extra }}]`{% else %}—{% endif %} | {% if m.checkpoint %}`{{ m.checkpoint.split('@')[0] }}`{% else %}—{% endif %} |
{% endfor %}

</div>

## Diagnostic models ({{ n('diagnostic') }})

Diagnostic models derive new quantities from existing fields — precipitation,
downscaling to higher resolution, cyclone tracking, and other decision-ready variables.

<div class="e2s-table" markdown>

| Model | Coverage | Type | Products | Rec. VRAM | Install |
| --- | --- | --- | --- | --- | --- |
{% for m in entries('diagnostic') -%}
| [`{{ m.name }}`](https://nvidia.github.io/earth2studio/modules/generated/models/dx/earth2studio.models.dx.{{ m.name }}.html) | {{ m.badges.region | join(', ') | upper if m.badges.region else '—' }} | {{ m.badges['class'] | join(', ') | upper if m.badges['class'] else '—' }} | {{ m.badges['product'] | join(', ') if m.badges['product'] else '—' }} | {{ m.badges.gpu | join(', ') | upper if m.badges.gpu else '—' }} | {% if m.extra %}`[{{ m.extra }}]`{% else %}—{% endif %} |
{% endfor %}

</div>

## Data assimilation models ({{ n('data_assimilation') }})

{% for m in entries('data_assimilation') -%}
- **`{{ m.name }}`** — {{ m.summary | truncate(150) }}
{% endfor %}

---

**Legend** — *Type*: MRF medium-range forecast · NWC nowcasting · DS downscaling ·
S2S subseasonal-to-seasonal · CM climate · DA data assimilation.
*Install*: the pip extra, e.g. `pip install earth2studio[fcn3]`.

[Full API reference :octicons-arrow-right-24:](https://nvidia.github.io/earth2studio/modules/models_px.html){ .md-button }
