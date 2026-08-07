# Ecosystem

Earth2Studio is the inference side of the NVIDIA Earth-2 platform, and is
built to interoperate with the broader scientific Python stack.

## NVIDIA Earth-2 and PhysicsNeMo

[PhysicsNeMo](https://docs.nvidia.com/physicsnemo/latest/index.html) trains
physics-AI models; Earth2Studio deploys and operationalizes them for weather
and climate. NVIDIA's open Earth-2 models (FourCastNet, SFNO, StormCast, and
others) flow directly into the Earth2Studio model zoo.

## Framework-agnostic by design

The toolkit is designed to ride on top of different AI frameworks and model
architectures — models from Google DeepMind, ECMWF, Microsoft, Huawei, and
the research community run behind the same interface as NVIDIA's own.

## Standard scientific formats

Outputs stream to the formats the community already uses — including Zarr and
NetCDF — so results plug into existing analysis stacks (xarray and friends)
without conversion steps.

## Agent-ready skills

Earth2Studio ships skills for coding agents (Claude, Codex, OpenCode, and
others) that automate environment setup, model discovery, data fetching, and
first forecasts:

```bash
npx skills add NVIDIA/skills --skill earth2studio-install
npx skills add NVIDIA/skills --skill earth2studio-discover
npx skills add NVIDIA/skills --skill earth2studio-data-fetch
npx skills add NVIDIA/skills --skill earth2studio-deterministic-forecast
```

[NVIDIA Skills catalog :octicons-arrow-right-24:](https://build.nvidia.com/skills?q=earth2studio){ .md-button }
