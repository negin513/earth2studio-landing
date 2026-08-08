---
title: Earth2Studio
hide:
  - navigation
  - toc
---

<!-- ═══ 1. HERO — split layout on dark band ═══ -->
<div class="e2s-bleed e2s-hero2" markdown>
<div class="e2s-hero2__inner" markdown>
<div class="e2s-hero2__text" markdown>

<h1>Earth2Studio<br><em>Unified platform for AI in Earth System Sciences</em></h1>

Run and verify AI-driven forecasts of the Earth system — on your own
infrastructure. **40+ open models** behind one Python API.

[Get started](#quickstart){ .md-button .md-button--primary }
[Try it in your browser :octicons-link-external-16:](https://build.nvidia.com/nvidia/fourcastnet){ .md-button }

<p class="e2s-pip"><code>uv add "earth2studio @ git+https://github.com/NVIDIA/earth2studio.git@0.17.0"</code></p>

<p class="e2s-badges">
<a href="https://pypi.org/project/earth2studio/"><img src="https://img.shields.io/pypi/v/earth2studio?color=76b900&label=PyPI" alt="PyPI version"></a>
<a href="https://pypi.org/project/earth2studio/"><img src="https://img.shields.io/pypi/dm/earth2studio?color=76b900&label=downloads" alt="Monthly downloads"></a>
<a href="https://github.com/NVIDIA/earth2studio/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-76b900" alt="Apache-2.0 license"></a>
</p>

</div>
<div class="e2s-hero2__img" markdown>

![Global AI weather forecast rendered by Earth2Studio](https://huggingface.co/datasets/nvidia/earth2studio-assets/resolve/main/readme/v2/earth2studio-readme-hero.png?v2)

</div>
</div>
</div>

<!-- ═══ 2. TRUST BAND ═══ -->
<div class="e2s-bleed e2s-trust">
  <span>Part of NVIDIA Earth-2</span>
  <span>Apache-2.0 open source</span>
  <span>Global forecasts on a single GPU</span>
  <span>Production-ready pipelines</span>
</div>

<!-- ═══ 3. WHY IT MATTERS ═══ -->
## From anticipating extremes to exploring climate futures { .e2s-centered #why-it-matters }

<p class="e2s-centered">AI Earth system models change the economics of
forecasting — and what becomes possible when a forecast costs seconds
instead of supercomputer-hours.</p>

<div class="grid cards" markdown>

- :fontawesome-solid-bolt: **Anticipate**

    ---

    Ensemble forecasts at a scale traditional NWP can't afford —
    quantify tail risk for the extreme events that matter most.

- :fontawesome-solid-seedling: **Adapt**

    ---

    Downscaled, decision-ready projections for energy, agriculture,
    insurance, and infrastructure planning.

- :fontawesome-solid-rocket: **Advance**

    ---

    An open, level playing field for evaluating the next generation of
    Earth system AI — in service of planetary resilience.

</div>

<!-- ═══ 4. THE PLATFORM — four named pillars ═══ -->
## The platform { .e2s-centered }

<p class="e2s-centered">Four interchangeable building blocks. Swap any of
them without rewriting the rest.</p>

<div class="grid cards e2s-cols-4" markdown>

- :fontawesome-solid-satellite: **AI-Ready Earth System Data Sources**

    ---

    Reanalysis, operational forecasts, and satellite and in-situ
    observations — analysis-ready and cloud-optimized, streamed on demand.

    [Explore data →](user-guide/data.md)

- :fontawesome-solid-brain: **Earth System Model Zoo**

    ---

    The largest open collection of prognostic and diagnostic Earth system
    AI models — from medium-range weather to subseasonal scales — with
    automatic checkpoint fetching.

    [Explore models →](user-guide/models.md)

    <span class="e2s-count">40+ AI models</span>

- :fontawesome-solid-diagram-project: **Composable Inference Pipelines**

    ---

    Deterministic, ensemble, and downscaling workflows built from
    interchangeable blocks: models, data, perturbations, statistics, IO.

    [Explore workflows →](user-guide/workflows.md)

- :fontawesome-solid-circle-check: **Trusted Verification**

    ---

    GPU-accelerated deterministic and probabilistic metrics to score
    every forecast against analysis and real observations.

    [Explore verification →](user-guide/verification.md)

</div>

<!-- ═══ 5. QUICKSTART — tabbed code ═══ -->
## Your first forecast in five lines { .e2s-centered }

<p class="e2s-centered">A data source, a model, a run function — checkpoints,
regridding, coordinates, and device placement are handled for you.</p>

<div class="e2s-quick" markdown>

=== "Deterministic"

    ```python
    from earth2studio.models.px import SFNO
    from earth2studio.data import GFS
    from earth2studio.io import ZarrBackend
    from earth2studio.run import deterministic

    model = SFNO.load_model(SFNO.load_default_package())
    deterministic(["2024-01-01"], 10, model, GFS(), ZarrBackend())
    ```

=== "Ensemble"

    ```python
    from earth2studio.models.px import SFNO
    from earth2studio.data import GFS
    from earth2studio.io import ZarrBackend
    from earth2studio.perturbation import SphericalGaussian
    from earth2studio.run import ensemble

    model = SFNO.load_model(SFNO.load_default_package())
    ensemble(["2024-01-01"], 10, 8, model, GFS(), ZarrBackend(), SphericalGaussian())
    ```

=== "Diagnostics"

    ```python
    from earth2studio.models.px import SFNO
    from earth2studio.models.dx import PrecipitationAFNO
    from earth2studio.data import GFS
    from earth2studio.io import ZarrBackend
    from earth2studio.run import diagnostic

    px = SFNO.load_model(SFNO.load_default_package())
    dx = PrecipitationAFNO.load_model(PrecipitationAFNO.load_default_package())
    diagnostic(["2024-01-01"], 10, px, dx, GFS(), ZarrBackend())
    ```

</div>

- :fontawesome-solid-check: Checkpoints fetch automatically
- :fontawesome-solid-check: Regridding and coordinates handled
- :fontawesome-solid-check: Swapping models is a one-line change

<!-- ═══ 6. SPOTLIGHTS ═══ -->
## More than a model runner { .e2s-centered }

<div class="e2s-spot" markdown>
<div class="e2s-spot__media" markdown>

![Earth2Studio data sources](https://huggingface.co/datasets/nvidia/earth2studio-assets/resolve/main/readme/v2/earth2studio-readme-data-sources.png?v3)

</div>
<div class="e2s-spot__body" markdown>

### AI-ready Earth system data, without the data engineering

Reanalysis, operational forecasts, and satellite and in-situ observations
pulled straight from cloud stores into your pipeline — analysis-ready, with
regridding and coordinates handled for you.

[Explore data →](user-guide/data.md)

</div>
</div>

<div class="e2s-spot" markdown>
<div class="e2s-spot__media" markdown>

![The Earth2Studio model zoo](https://huggingface.co/datasets/nvidia/earth2studio-assets/resolve/main/readme/v2/earth2studio-readme-model-zoo.png?v3)

</div>
<div class="e2s-spot__body" markdown>

### The largest open model zoo

Prognostic and diagnostic Earth system AI models from across the field,
packaged and ready to run behind one interface — with new models added
continuously.

[Explore models →](user-guide/models.md)

</div>
</div>

<div class="e2s-spot" markdown>
<div class="e2s-spot__media" markdown>

![Composable Earth2Studio pipelines](https://huggingface.co/datasets/nvidia/earth2studio-assets/resolve/main/readme/v2/earth2studio-readme-composability.png?v2)

</div>
<div class="e2s-spot__body" markdown>

### From experiment to operations

Chain data sources, models, perturbations, diagnostics, and statistics into
production pipelines — then swap any piece without rewriting the rest.
Graduate from a notebook to recipes like huge ensembles and S2S forecasting.

[Explore workflows →](user-guide/workflows.md)

</div>
</div>

<!-- ═══ 7. INSTITUTIONS + MODEL TEASER ═══ -->
## Models from leading institutions { .e2s-centered }

<p class="e2s-centered">The Earth2Studio model zoo includes Earth system AI
models developed by research teams across industry and academia — the same
model families powering national forecasting and digital-twin initiatives.</p>

<div class="e2s-logos">
  <img src="assets/images/logos/nvidia.svg" alt="NVIDIA" title="NVIDIA">
  <img src="assets/images/logos/deepmind.svg" alt="Google DeepMind" title="Google DeepMind">
  <img src="assets/images/logos/ecmwf.svg" alt="ECMWF" title="ECMWF">
  <img src="assets/images/logos/microsoft.svg" alt="Microsoft" title="Microsoft">
  <img src="assets/images/logos/huawei.svg" alt="Huawei" title="Huawei">
  <img src="assets/images/logos/fudan.svg" alt="Fudan University" title="Fudan University">
  <img src="assets/images/logos/ai2.svg" alt="Allen Institute for AI" title="Allen Institute for AI">
  <span>Shanghai AI Lab</span>
</div>

<div class="e2s-centered" markdown>
[Browse the full model zoo :octicons-arrow-right-24:](user-guide/models.md){ .md-button }
</div>

<!-- ═══ 8. ECOSYSTEM ═══ -->
## Built open, connected everywhere { .e2s-centered }

<div class="grid cards" markdown>

- :fontawesome-solid-cubes: **Train with PhysicsNeMo**

    ---

    PhysicsNeMo trains physics-AI models; Earth2Studio deploys them.
    NVIDIA's open Earth-2 models flow directly into the zoo.

    [PhysicsNeMo →](https://docs.nvidia.com/physicsnemo/latest/index.html)

- :fontawesome-solid-layer-group: **Speaks the scientific stack**

    ---

    Outputs stream to Zarr and NetCDF, landing directly in the
    xarray / Pangeo analysis ecosystem — no conversion steps.

    [Ecosystem →](user-guide/ecosystem.md)

- :fontawesome-solid-robot: **Agent-ready**

    ---

    Official skills let coding agents install Earth2Studio, pick a model,
    fetch data, and run a first forecast automatically.

    [NVIDIA Skills →](https://build.nvidia.com/skills?q=earth2studio)

</div>

<!-- ═══ 9. WHO IT'S FOR ═══ -->
## Who it's for { .e2s-centered }

<div class="grid cards" markdown>

- :fontawesome-solid-microscope: **Scientists & researchers**

    ---

    Benchmark models on identical data through one unified API, and
    verify results with built-in metrics.

- :fontawesome-solid-satellite-dish: **Met services & agencies**

    ---

    Sovereign forecasting capability — run, fine-tune, and deploy
    independently, on infrastructure you control.

- :fontawesome-solid-building: **Enterprises**

    ---

    Bring forecasting in-house. Run ensembles for risk quantification in
    energy, insurance, logistics, and agriculture.

- :fontawesome-solid-code: **Developers**

    ---

    Build weather-aware products on a composable Python SDK — with
    agent-ready skills for automated setup.

- :fontawesome-solid-graduation-cap: **Educators & students**

    ---

    A free, open on-ramp to modern Earth system AI that runs on a
    single GPU.

</div>

<!-- ═══ 11. CITATION + MISSION ═══ -->
## Citing Earth2Studio { .e2s-centered }

```bibtex
@software{earth2studio2024,
  author  = {{Earth2Studio Contributors}},
  title   = {{NVIDIA Earth2Studio}},
  url     = {https://github.com/NVIDIA/earth2studio},
  year    = {2024}
}
```

<div class="e2s-centered" markdown>

*Our mission is to enable everyone to build, research, and explore AI-driven
weather and climate science.*

</div>
