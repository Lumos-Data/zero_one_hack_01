# Forecast Artifacts

Downloaded via `GET /api/v1/forecasts/:id/artifacts/:name`

## Artifact files

| File | Always | When present |
|------|--------|-------------|
| `forecast.json` | yes | Always |
| `external_signals.json` | yes | Always |
| `backtest_metrics.json` | no | `backtest: true` |
| `backtest_trajectories.json` | no | `backtest: true` |

Envelope: `{ "version": "1.1", "data": {...} }`

---

## forecast.json

```json
{
  "version": "1.1",
  "data": {
    "forecast_horizon": 6,
    "forecast_start": "2026-01-01",
    "forecast_end": "2026-06-01",
    "forecast_series": {
      "2026-01-01": {
        "forecast": 1234.56,
        "quantile_forecast": {
          "0.1": 1100.0,
          "0.5": 1234.5,
          "0.9": 1380.7
        }
      }
    }
  }
}
```

- `forecast` = point estimate (same as quantile 0.5 when probabilistic)
- `quantile_forecast.0.1` = pessimistic (10th percentile)
- `quantile_forecast.0.5` = median
- `quantile_forecast.0.9` = optimistic (90th percentile)

---

## external_signals.json

Map of driver UUID → driver info:

```json
{
  "f0e1d2c3-...": {
    "driver_name": "EU industrial production index",
    "importance": {
      "horizon_1": { "0.0": 87.4, "1.0": 65.2 },
      "horizon_2": { "0.0": 80.1 },
      "overall": { "mean": 73.5, "min": 41.0, "max": 87.4 }
    },
    "direction": {
      "horizon_0": { "0.0": 0.62 },
      "horizon_1": { "0.0": 0.58, "1.0": 0.41 },
      "overall": { "mean": 0.55, "min": 0.41, "max": 0.62 }
    },
    "pearson_correlation": {
      "overall": { "mean": 0.47, "min": 0.31, "max": 0.59 },
      "lag_6": 0.59,
      "lag_12": 0.31
    }
  }
}
```

Fields per driver:
- `driver_name` — human-readable label
- `importance` — normalized importance scores per horizon
- `direction` — signed correlation per horizon/lag
- `pearson_correlation` — per-lag and aggregated correlation

---

## backtest_metrics.json

```json
{
  "6m":  { "metrics": {...}, "tests": {}, "forecast_start": "...", "forecast_end": "..." },
  "12m": { "metrics": {...}, "tests": {}, "forecast_start": "...", "forecast_end": "..." },
  "24m": { ... },
  "60m": { ... }
}
```

Windows with no completed folds are omitted. `metrics` contains MAPE, RMSE averaged across folds.

---

## backtest_trajectories.json

Array of trajectory objects, sorted by forecast_start ascending:

```json
[
  {
    "forecast_start": "2025-05-01",
    "forecast_end": "2025-10-01",
    "metrics": { "mape": 0.061, "rmse": 142.7 },
    "forecast_series": {
      "2025-05-01": { "actual": 1180.0, "forecast": 1163.4 },
      "2025-06-01": { "actual": 1212.5, "forecast": 1207.9 }
    }
  }
]
```

- Only last 12 months of trajectories included
- `actual` is null if no observation for that date

## Errors

| Code | Cause |
|------|-------|
| 401 | Bad token |
| 404 | Job not found or artifact unavailable |
| 409 | Job not completed yet |
| 413 | Artifact > 100 MiB |
