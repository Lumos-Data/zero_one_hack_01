# POST /api/v1/forecasts — Submit Forecast Job

**Type:** async (returns 202 with job_id)
**Billed:** yes (base + time-based)

## Request Body

All fields top-level:

| Field | Required | Type | Rules |
|-------|----------|------|-------|
| `pipeline_version` | yes | string | must be exactly `"v1"` |
| `frequency` | yes | string | only `"monthly"` supported |
| `soft_horizon` | at least one | int | 1-12, ideal horizon |
| `hard_horizon` | at least one | int | 1-12, minimum acceptable horizon |
| `backtest` | no | bool | default `false`, enables backtest artifacts |
| `recency_factor` | yes | number | 0.0-1.0, news recency weighting |
| `strictly_positive` | no | bool | default `false`, clamps forecast >= 0 |
| `timeseries_metadata` | yes | object | see below |
| `timeseries` | yes | object | `YYYY-MM-DD` → number |
| `filters` | no | object | categories, regions, limit |

### `soft_horizon` vs `hard_horizon`

- `soft_horizon`: ideal length, pipeline tries first
- `hard_horizon`: minimum acceptable, pipeline steps down to this
- If both: `hard_horizon <= soft_horizon`
- When only one given, `horizonMax = that value`

### `recency_factor`

- `0.0` = broader historical news window (up to Jan 2020)
- `1.0` = strong emphasis on recent news (up to latest week)
- Significant impact on driver selection and forecast quality

### `strictly_positive`

- `true`: input values must be >= 0 (422 if negative), output clamped at 0
- `false`: negative values allowed in both input and output

### `timeseries_metadata`

| Field | Required | Rules |
|-------|----------|-------|
| `title` | yes | 20-511 bytes |
| `description` | no | <= 2048 bytes |
| `keywords` | no | array, <= 20 items, each <= 255 bytes |

**keywords are CRITICAL** — strongly affect driver selection and forecast quality. Include both direct terms and broader domain knowledge.

### `timeseries`

Object: `{ "YYYY-MM-DD": number, ... }`

Rules:
1. Keys must be first day of month: `YYYY-MM-01`
2. No gaps in monthly grid
3. Values must be finite (no NaN/Inf)
4. Non-empty

Minimum data points by horizon:

| horizonMax | Min monthly points |
|------------|-------------------|
| 1-3 | 40 |
| 4-6 | **60** |
| 7-12 | 120 |

Recency: latest observation must be within past 12 months.

### `filters` (optional)

| Field | Type | Rules |
|-------|------|-------|
| `categories[]` | int[] | category ids (1-9999) |
| `regions[]` | int[] | region ids (1-9999) |
| `limit` | int | 0-1000, controls how many drivers considered |

## Response (202 Accepted)

```json
{
  "job_id": "c7f2d8a9-...",
  "poll_url": "/api/v1/forecasts/c7f2d8a9-..."
}
```

## Errors

| Code | Cause |
|------|-------|
| 402 | Insufficient balance for hold |
| 422 | Validation failure (one detail) |
| 429 | Rate limit or concurrent job cap |
| 413 | Body over 2 MiB |
