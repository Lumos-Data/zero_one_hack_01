# Authentication

## Method

All API calls use **Bearer token** auth:

```
Authorization: Bearer sk_ops_...
```

## Setup

1. Go to https://sybilion.dev/keys
2. Create API key (shown only once, starts with `sk_ops_`)
3. Store in env var:

```bash
export SYBILION_API_TOKEN="sk_ops_..."
```

## Python SDK

Automatically reads `SYBILION_API_TOKEN` from environment:

```python
from sybilion import Client
client = Client()  # reads SYBILION_API_TOKEN automatically
```

Or pass explicitly:

```python
client = Client(token="sk_ops_...")
```

## Errors

- `401` — missing or invalid token
- MCP (Claude/ChatGPT) uses OAuth instead of API key
