# AI-Ready Earth System Data Sources

Earth2Studio provides on-demand access to AI-ready Earth system data straight
from cloud stores — analysis-ready and cloud-optimized — no manual downloads, no preprocessing scripts. Every data
source implements the same interface, so pipelines can swap sources without
code changes.

## Reanalysis

Historical, analysis-ready atmospheric state for training-style inputs and
hindcast studies.

- **ERA5 (ARCO)** — cloud-optimized ERA5 reanalysis
- **CDS** — Copernicus Climate Data Store access
- **CMIP6** — climate model intercomparison data

## Operational forecasts and analysis

Near-real-time initial conditions for live forecasting.

- **GFS / GEFS** — NOAA global deterministic and ensemble systems
- **ECMWF (IFS)** — open operational forecast data
- **HRRR** — high-resolution rapid refresh over CONUS

## Observations

In-situ and satellite observation sources for verification and data
assimilation research.

- **Conventional observations** — NNJA and real-time GDAS conventional obs
- **Satellite instruments** — GOES, Himawari, Meteosat, JPSS, and MetOp readers
- **Station and event records** — ISD surface stations, GHCN, IBTrACS cyclone tracks

[Full data source catalog :octicons-arrow-right-24:](https://nvidia.github.io/earth2studio/modules/datasources.html){ .md-button }
