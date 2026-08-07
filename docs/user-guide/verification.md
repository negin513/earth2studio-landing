# Verification

A forecast is only useful if you can trust it. Earth2Studio includes a
statistics and metrics suite for verifying AI forecasts against analysis and
observations — GPU-accelerated and composable into the same pipelines that
produce the forecasts.

## Deterministic metrics

Score a single forecast against the verifying truth.

- **ACC** — anomaly correlation coefficient against climatology
- **RMSE and moment statistics** — error magnitude and distributional moments
- **FSS** — fractions skill score for spatial verification
- **LSD** — log spectral distance for assessing effective resolution

## Probabilistic metrics

Score ensemble forecasts on calibration and sharpness.

- **CRPS** — continuous ranked probability score
- **Brier score** — probabilistic event verification
- **Energy score** — multivariate ensemble verification

## Verification against observations

Data sources for surface stations, satellite instruments, and conventional
observations let you verify against what was actually measured — not just
against another model analysis.

[Statistics API reference :octicons-arrow-right-24:](https://nvidia.github.io/earth2studio/modules/statistics.html){ .md-button }
