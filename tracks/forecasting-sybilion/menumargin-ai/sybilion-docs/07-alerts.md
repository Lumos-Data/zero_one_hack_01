# POST /api/v1/alerts — Alert Detection

**Type:** sync (returns immediately)
**Billed:** yes

Detect alerts/anomalies against provided timeseries metadata.

## Request Body

| Field | Required | Rules |
|-------|----------|-------|
| `metadata.title` | yes | 20-511 characters |
| `metadata.description` | no | <= 2048 characters |
| `metadata.keywords` | no | <= 20 items, each <= 255 chars |
| `context_enriched` | yes | bool, true if metadata already enriched |
| `date_from` | no | YYYY-MM-DD, lower bound |
| `date_to` | no | YYYY-MM-DD, upper bound >= date_from |
| `filters` | no | same as drivers/forecasts |
| `filters.limit` | no | 0-100, default 100 |

## Response

```json
{
  "alerts": [
    {
      "name": "Brent Crude Oil",
      "pct_change": 12.4,
      "trending": true,
      "news": [
        {
          "title": "Oil prices surge on supply concerns",
          "description": "Brent crude rose sharply after...",
          "url": "https://example.com/article",
          "published_at": "2026-04-30T08:00:00Z",
          "source_name": "Reuters",
          "category": "Energy",
          "trending": true
        }
      ]
    }
  ]
}
```

## Use for MenuMargin

Could be used to detect sudden price spikes in ingredients and trigger urgent recommendations.
