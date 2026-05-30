# GET /api/v1/forecasts/:id — Poll Job Status

**Type:** sync, not billed

Poll until `status == "completed"`, then download artifacts.

## Response

```json
{
  "job_id": "...",
  "pipeline_type": "forecast",
  "status": "completed",
  "created_at": "2026-04-30T10:00:00Z",
  "settled_at": "2026-04-30T10:05:42Z",
  "settled": true,
  "eur_cents_final": 3,
  "artifacts": [
    {
      "name": "forecast.json",
      "size": 18342,
      "content_type": "application/json",
      "href": "/api/v1/forecasts/.../artifacts/forecast.json"
    }
  ]
}
```

## Status values

- `queued` — waiting to start
- `running` — pipeline executing
- `completed` — done, artifacts available
- `failed` — error, see `pipeline_error`
- `canceled` — cancelled

## Fields

| Field | Always present | Notes |
|-------|---------------|-------|
| `job_id` | yes | UUID |
| `pipeline_type` | yes | always `"forecast"` |
| `status` | yes | one of above |
| `created_at` | yes | RFC3339 |
| `settled_at` | yes | null until settled |
| `settled` | yes | true once settled |
| `eur_cents_final` | yes | null before settled |
| `artifacts` | no | only when completed + settled |
| `pipeline_error` | no | only when failed/canceled |
| `terminal_reason` | no | only when failed/canceled |

## Python SDK polling

```python
job = client.wait_forecast(job_id, poll_s=10.0, timeout_s=3600.0)
# returns as soon as settled (completed/failed/canceled)
```

## Errors

- `401` — bad token
- `404` — unknown id or outside visibility window
