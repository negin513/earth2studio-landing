# Models

Earth2Studio ships the largest open collection of AI weather and climate
models, all behind one unified interface. Checkpoints download automatically —
pick a model and run.

## Prognostic models

Prognostic models perform time integration: given the atmospheric state now,
they predict the state at the next step, and roll forward to build a forecast.

| Model | Origin |
| --- | --- |
| **FourCastNet / FCN3** | NVIDIA |
| **SFNO** | NVIDIA |
| **StormCast** | NVIDIA (regional, km-scale) |
| **GraphCast** | Google DeepMind |
| **GenCast (mini)** | Google DeepMind |
| **Pangu-Weather** | Huawei |
| **Aurora** | Microsoft |
| **AIFS** | ECMWF |
| **FuXi** | Fudan University |
| **FengWu** | Shanghai AI Lab |
| **DLWP / DLESyM** | University of Washington |
| **ACE2** | Allen Institute for AI |

…and more, with new models added continuously.

## Diagnostic models

Diagnostic models derive new quantities from existing forecast fields —
precipitation estimation, downscaling to higher resolution, cyclone tracking,
and other decision-ready variables.

## One interface, any model

```python
# Swapping models is a one-line change
from earth2studio.models.px import SFNO      # or GraphCast, Pangu, Aurora, ...
model = SFNO.load_model(SFNO.load_default_package())
```

[Full model catalog :octicons-arrow-right-24:](https://nvidia.github.io/earth2studio/modules/models_px.html){ .md-button }
