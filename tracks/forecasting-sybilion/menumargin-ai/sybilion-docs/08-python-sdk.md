# Python SDK Reference

**Package:** `sybilion` on PyPI
**Requires:** Python 3.10+
**Install:** `pip install sybilion`

## Client setup

```python
import os
from sybilion import Client

# Auto-reads SYBILION_API_TOKEN from env
client = Client()

# Or explicit
client = Client(token=os.environ["SYBILION_API_TOKEN"])

# Custom base URL
client = Client(base_url="https://custom.api.url")
```

Base URL resolution order:
1. `base_url` argument
2. `SYBILION_API_BASE_URL` env var
3. Default: `https://api.sybilion.dev`

## Methods

| Method | Endpoint | Returns |
|--------|----------|---------|
| `client.me()` | GET /api/v1/me | account info |
| `client.submit_forecast(body)` | POST /api/v1/forecasts | submit response |
| `client.get_forecast(id)` | GET /api/v1/forecasts/{id} | job status |
| `client.get_forecast_artifact(id, name)` | GET /api/v1/forecasts/{id}/artifacts/{name} | bytes |
| `client.wait_forecast(job_id, poll_s, timeout_s)` | polling helper | settled job |
| `client.get_drivers(body)` | POST /api/v1/drivers | drivers response |
| `client.get_alerts(...)` | POST /api/v1/alerts | alerts list |
| `client.list_regions()` | GET /api/v1/regions | regions list |
| `client.list_categories()` | GET /api/v1/categories | categories list |
| `client.list_jobs(...)` | GET /api/v1/jobs | jobs list |
| `client.get_usage(...)` | GET /api/v1/usage | usage events |

## Full forecast workflow

```python
import json
from sybilion import Client

client = Client()

# Load request body
with open("forecast_body.json") as f:
    body = json.load(f)

# Submit
submit = client.submit_forecast(body)
print("job_id:", submit.job_id)

# Wait for completion
job = client.wait_forecast(submit.job_id, poll_s=10.0, timeout_s=3600.0)
print("status:", job.status, "cost:", job.eur_cents_final, "cents")

# Download artifacts
forecast_data = json.loads(client.get_forecast_artifact(submit.job_id, "forecast.json"))
signals_data = json.loads(client.get_forecast_artifact(submit.job_id, "external_signals.json"))

# Parse forecast
for date, values in forecast_data["data"]["forecast_series"].items():
    print(f"{date}: {values['forecast']:.2f} (q10={values['quantile_forecast']['0.1']:.2f})")
```

## wait_forecast behavior

- Polls every `poll_s` seconds
- Returns as soon as `settled == True` (completed/failed/canceled)
- Raises `TimeoutError` if deadline exceeded (job continues on server)

## Error handling

```python
from sybilion import (
    ApiException,
    BadRequestException,      # 400
    UnauthorizedException,    # 401
    NotFoundException,        # 404
    ConflictException,        # 409
    UnprocessableEntityException,  # 422
    ServiceException,         # 5xx
)

try:
    job = client.submit_forecast(body)
except UnprocessableEntityException as exc:
    print("validation failed:", exc.body)
except ApiException as exc:
    print("HTTP", exc.status, exc.reason)
```

## Pagination helpers

```python
for page in client.iter_usage_pages(limit=100):
    for ev in page.usage_events:
        print(ev.id)

for page in client.iter_jobs_pages(limit=100, status="completed"):
    for job in page.jobs:
        print(job.job_id)
```
