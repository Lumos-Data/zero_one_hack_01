# Errors & Limits

## Error codes

| Code | When | Body format |
|------|------|-------------|
| 400 | Malformed JSON, invalid query params | standard |
| 401 | Missing/invalid bearer token | standard |
| 402 | Insufficient balance | `{"error": "insufficient available credits for hold"}` |
| 404 | Not found / outside visibility window | standard |
| 409 | Job not completed (artifact download) | standard |
| 413 | Body > 2 MiB or artifact > 100 MiB | standard |
| 422 | Validation failure | `{"error": "validation_failed", "details": [{"field": "...", "message": "..."}]}` |
| 429 | Rate limit or concurrent job cap | message varies |
| 502 | Upstream transport error | standard |
| 503 | Backend unavailable | standard |

## 422 validation

Only ONE detail returned per request (fail-fast):

```json
{
  "error": "validation_failed",
  "details": [
    { "field": "soft_horizon", "message": "soft_horizon must be between 1 and 12" }
  ]
}
```

## 402 balance

Balance in EUR cents on `GET /api/v1/me`:
- `available_eur_cents` — what you can spend now
- `balance_eur_cents` — total including holds

Forecast hold = estimate of max cost, released and replaced by actual charge on settle.

## 429 rate limits

Three independent caps per tier:
1. Requests per minute (general) — all endpoints
2. Requests per minute (sync billed) — drivers + alerts
3. Concurrent forecast jobs — in-flight (queued/running)

## Concurrency vs holds

- Concurrent cap counts job statuses (queued/running)
- Balance holds reduce `available_eur_cents` separately
- Can hit 429 for concurrency with positive balance
- Can hit 402 on balance with zero running jobs (holds settling)
