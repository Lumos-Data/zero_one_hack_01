# Sybilion API — Overview

**Base URL:** `https://api.sybilion.dev`
**Docs:** `https://sybilion.dev/docs`
**OpenAPI spec:** `https://api.sybilion.dev/docs`
**Python SDK:** `pip install sybilion`

## What is Sybilion

Forecasting-as-a-Service. You give it a monthly time series (40-120+ data points), it returns:
- Point forecasts with quantile bands (0.1, 0.5, 0.9)
- External driver attributions (what macro signals influence the series)
- Optional backtest metrics (MAPE, RMSE)

## API Endpoints

| Method | Endpoint | Type | Billed | Description |
|--------|----------|------|--------|-------------|
| POST | `/api/v1/forecasts` | async | yes | Submit forecast job, returns job_id |
| GET | `/api/v1/forecasts/:id` | sync | no | Poll job status |
| GET | `/api/v1/forecasts/:id/artifacts/:name` | sync | no | Download result files |
| POST | `/api/v1/drivers` | sync | yes | Get driver recommendations (no forecast) |
| POST | `/api/v1/alerts` | sync | yes | Alert detection on metadata |
| GET | `/api/v1/regions` | sync | no | List region filter ids |
| GET | `/api/v1/categories` | sync | no | List category filter ids |
| GET | `/api/v1/me` | sync | no | Account info & balance |
| GET | `/api/v1/usage` | sync | no | Billing history |
| GET | `/api/v1/jobs` | sync | no | List all jobs |

## Async Forecast Flow

```
1. POST /api/v1/forecasts  →  202 Accepted  →  { job_id, poll_url }
2. GET  /api/v1/forecasts/{job_id}  →  poll until status == "completed"
3. GET  /api/v1/forecasts/{job_id}/artifacts/forecast.json  →  download results
```

Python SDK handles this with `client.submit_forecast()` + `client.wait_forecast()`.

## Limits

- Forecast body max: **2 MiB**
- Artifact stream max: **100 MiB**
- `frequency`: only `"monthly"` supported in v1
- `soft_horizon` / `hard_horizon`: integers 1-12
- Concurrent forecast jobs: depends on tier
