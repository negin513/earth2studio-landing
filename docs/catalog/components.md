# Pipeline components

The interchangeable blocks a workflow is built from, beyond models and data.

!!! info "Generated from source"
    Generated from the Earth2Studio source. It cannot drift from the code.

## Perturbations ({{ n('perturbations') }})

Perturbation methods generate ensemble members by perturbing the initial state.

{% for p in entries('perturbations') -%}
- **`{{ p.name }}`** — {{ p.summary | truncate(140) }}
{% endfor %}

## Statistics and metrics ({{ n('statistics') }})

Scoring functions for verifying forecasts against analysis or observations.

{% for s in entries('statistics') -%}
- **`{{ s.name }}`** — {{ s.summary | truncate(140) if s.summary else '' }}
{% endfor %}

## IO backends ({{ n('io_backends') }})

Where results are written.

{% for i in entries('io_backends') -%}
- **`{{ i.name }}`** — {{ i.summary | truncate(140) }}
{% endfor %}

---

[Perturbation API](https://nvidia.github.io/earth2studio/modules/perturbation.html){ .md-button }
[Statistics API](https://nvidia.github.io/earth2studio/modules/statistics.html){ .md-button }
