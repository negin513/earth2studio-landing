---
hide:
  - navigation
  - toc
---

# Earth2Studio { .e2s-center-title }

<div class="e2s-hero-min" markdown>

**The open toolkit for AI Earth system models.**

A unified API, the largest open zoo of AI weather and climate models, and
composable inference pipelines — built by NVIDIA, open to everyone.

[Get started :octicons-arrow-right-24:](user-guide/index.md){ .md-button .md-button--primary }
[GitHub](https://github.com/NVIDIA/earth2studio){ .md-button }

</div>

<div class="grid cards" markdown>

- 🧠 **Models**

    ---

    The largest open collection of AI weather and climate models —
    prognostic and diagnostic — behind one unified interface, with
    automatic checkpoint fetching.

    [Explore models →](user-guide/models.md)

- 🌐 **Data**

    ---

    On-demand access to analysis, reanalysis, forecast, and observational
    data from cloud stores — no manual downloads or preprocessing.

    [Explore data →](user-guide/data.md)

- 🔁 **Workflows**

    ---

    Deterministic, ensemble, and downscaling pipelines composed from
    modular building blocks: models, data, perturbations, statistics, IO.

    [Explore workflows →](user-guide/workflows.md)

- ✅ **Verification**

    ---

    GPU-accelerated metrics for scoring forecasts — deterministic and
    probabilistic — against analysis and real observations.

    [Explore verification →](user-guide/verification.md)

</div>

## A forecast in a few lines

```python
from earth2studio.models.px import SFNO
from earth2studio.data import GFS
from earth2studio.run import deterministic

model = SFNO.load_model(SFNO.load_default_package())
deterministic(["2024-01-01"], 10, model, GFS(), io)  # 10-day global forecast
```

Checkpoints, regridding, coordinates, and device placement are handled for you.
Swap the model or the data source without touching the rest of the pipeline.

## Who it's for

<div class="grid cards" markdown>

- 🔬 **Scientists & researchers**

    ---

    Benchmark models against each other on identical data through one
    unified API. Prototype new pipelines without spending a month on
    infrastructure, and verify results with built-in metrics.

- 🏢 **Enterprises**

    ---

    Bring forecasting in-house. Run ensembles for risk quantification in
    energy, insurance, logistics, and agriculture — at a fraction of the
    cost of traditional numerical weather prediction.

- 💻 **Developers**

    ---

    Build weather-aware products on a composable, Apache-2.0 licensed
    Python SDK — with agent-ready skills for automated setup.

- 🎓 **Educators & students**

    ---

    A free, open on-ramp to modern AI weather modeling: pre-trained
    models, public data, and runnable examples that work on a single GPU.

</div>

---

*Our mission is to enable everyone to build, research, and explore AI-driven
weather and climate science.*

[Read the docs :octicons-arrow-right-24:](user-guide/index.md){ .md-button .md-button--primary }
