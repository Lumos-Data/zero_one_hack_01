# POST /api/v1/drivers — Driver Recommendations

**Type:** sync (returns immediately)
**Billed:** yes

Get recommended external drivers for a time series WITHOUT running a full forecast.

## Request Body

| Field | Required | Rules |
|-------|----------|-------|
| `version` | yes | must be `"v1"` |
| `recency_factor` | no | 0.0-1.0, default 0.5 |
| `timeseries_metadata` | yes | same rules as forecasts (title 20-511 bytes, keywords <= 20) |
| `filters` | no | same as forecasts |
| `timeseries` | no | if present, no monthly grid/min-length rules |

## Example

```json
{
  "version": "v1",
  "recency_factor": 0.5,
  "timeseries_metadata": {
    "title": "Olive Oil Consumer Price Index EU Monthly",
    "keywords": ["olive oil", "food price", "cooking oil"]
  },
  "filters": {
    "categories": [3],
    "regions": [42],
    "limit": 25
  }
}
```

## Response

```json
{
  "status": 200,
  "message": "ok",
  "data": {
    "drivers": [
      {
        "hash_id": "a1b2c3d4e5f6",
        "driver_name": "EU industrial production index",
        "score": 87.4
      }
    ]
  }
}
```

## Use cases

- Explore what macro signals affect an ingredient before committing to a full forecast
- Quick iteration on keywords and filters
- Build understanding for the "visible reasoning" requirement

## Errors

| Code | Cause |
|------|-------|
| 402 | Insufficient balance |
| 422 | Validation failure |
| 429 | Rate limit |
| 502 | Transport error |
| 503 | Feature not enabled |
