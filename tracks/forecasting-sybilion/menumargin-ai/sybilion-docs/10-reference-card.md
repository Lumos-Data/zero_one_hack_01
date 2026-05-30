# Quick Reference Card

## Our 6 Ingredients → Sybilion Requests

| # | Ingredient | COICOP | Sybilion title | keywords |
|---|-----------|--------|----------------|----------|
| 1 | pasta | CP01116 | "Pasta Products Consumer Price Index EU Monthly" | pasta, cereals, wheat, food price, Italian cuisine, semolina, durum |
| 2 | tomatoes | CP01171 | "Fresh Vegetables Consumer Price Index EU Monthly" | tomatoes, vegetables, fresh produce, Mediterranean, salads |
| 3 | cheese | CP01144 | "Cheese and Curd Consumer Price Index EU Monthly" | cheese, dairy, mozzarella, Italian cheese, parmesan, curd |
| 4 | olive oil | CP01153 | "Olive Oil Consumer Price Index EU Monthly" | olive oil, cooking oil, Mediterranean, extra virgin, EU HICP |
| 5 | eggs | CP01147 | "Eggs Consumer Price Index EU Monthly" | eggs, poultry, baking, protein, egg products |
| 6 | flour | CP01112 | "Flours and Cereals Consumer Price Index EU Monthly" | flour, wheat, baking, cereals, bread, grain |

## Common request template

```json
{
  "pipeline_version": "v1",
  "frequency": "monthly",
  "soft_horizon": 6,
  "hard_horizon": 3,
  "backtest": true,
  "recency_factor": 0.6,
  "strictly_positive": true,
  "timeseries_metadata": {
    "title": "<TITLE_FROM_TABLE_ABOVE>",
    "description": "Monthly HICP index for <ingredient> in EU27, base 2015=100. Source: Eurostat prc_hicp_midx.",
    "keywords": ["<KEYWORDS_FROM_TABLE_ABOVE>"]
  },
  "timeseries": {
    "2020-01-01": <value>,
    "2020-02-01": <value>,
    "..."
  }
}
```

## Forecast result structure

```
forecast.json
  └─ data.forecast_series
       └─ "2026-01-01"
            ├─ forecast: 125.3          ← point estimate
            └─ quantile_forecast
                 ├─ "0.1": 118.0        ← pessimistic (10th %ile)
                 ├─ "0.5": 125.3        ← median
                 └─ "0.9": 133.5        ← optimistic (90th %ile)

external_signals.json
  └─ driver_uuid
       ├─ driver_name: "EU industrial production"
       ├─ importance.overall.mean: 73.5
       ├─ direction.overall.mean: 0.55
       └─ pearson_correlation.lag_6: 0.59
```

## Data requirements

- Minimum 60 monthly points for 6-month horizon
- Latest point within last 12 months
- No gaps in monthly grid
- Dates: `YYYY-MM-01` format
- All values >= 0 when `strictly_positive: true`

## Python SDK cheat sheet

```python
from sybilion import Client
client = Client()  # reads SYBILION_API_TOKEN

# Full forecast
submit = client.submit_forecast(body)
job = client.wait_forecast(submit.job_id, poll_s=10.0)
forecast = json.loads(client.get_forecast_artifact(submit.job_id, "forecast.json"))
signals = json.loads(client.get_forecast_artifact(submit.job_id, "external_signals.json"))

# Drivers only (sync)
drivers = client.get_drivers(drivers_body)

# Catalogs (free, not billed)
regions = client.list_regions()
categories = client.list_categories()
```

## Pricing

- Forecasts: base fee + time-based (billed on 2xx only)
- Drivers: billed per call
- Alerts: billed per call
- Regions/Categories: FREE
- Balance: EUR cents, pre-charge hold on forecast submit
