# TME MCP Server

MCP server for [TME](https://www.tme.eu) — a major European electronic components distributor based in Poland.

Provides 13 tools: product search, details, pricing, stock levels, datasheets, delivery time, and URL generation.

## Prerequisites

1. Create an account at [developers.tme.eu](https://developers.tme.eu)
2. Register an application to get your **App Token** and **App Secret**

## Quick Start (Docker)

```bash
docker build -t tme-mcp .

docker run --rm -i \
  -e TME_APP_TOKEN="your-token" \
  -e TME_APP_SECRET="your-secret" \
  -e TME_COUNTRY=AT \
  -e TME_CURRENCY=EUR \
  tme-mcp:latest
```

## Claude Code Integration

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "tme": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "TME_APP_TOKEN",
        "-e", "TME_APP_SECRET",
        "-e", "TME_COUNTRY=AT",
        "-e", "TME_CURRENCY=EUR",
        "tme-mcp:latest"
      ]
    }
  }
}
```

Set `TME_APP_TOKEN` and `TME_APP_SECRET` as environment variables in your shell.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `TME_APP_TOKEN` | *(required)* | API token from developers.tme.eu |
| `TME_APP_SECRET` | *(required)* | HMAC secret for request signing |
| `TME_COUNTRY` | `PL` | Country code (e.g. `AT`, `DE`, `PL`) |
| `TME_LANGUAGE` | `EN` | Language code |
| `TME_CURRENCY` | `PLN` | Currency code (e.g. `EUR`, `PLN`) |

## Tools

### Search & Browse

| Tool | Description |
|---|---|
| `search_products` | Keyword/part number search, paginated |
| `autocomplete` | Type-ahead suggestions |
| `get_categories` | Category tree |
| `search_parameters` | Available filters for a category |

### Product Details

| Tool | Description |
|---|---|
| `get_products` | Full details, up to 50 symbols |
| `get_parameters` | Technical specs/attributes, up to 50 |
| `get_product_files` | Datasheets, photos, files |
| `get_similar_products` | Alternative parts |

### Pricing & Stock

| Tool | Description |
|---|---|
| `get_prices` | Pricing tiers, up to 50 |
| `get_stocks` | Inventory levels, up to 50 |
| `get_prices_and_stocks` | Combined pricing + stock |

### Other

| Tool | Description |
|---|---|
| `get_delivery_time` | Estimated delivery time |
| `generate_tme_url` | Build product page or cart URL |

## Authentication

TME uses HMAC-SHA1 per-request signing (not OAuth2). Each API call is individually signed using your App Secret. No token refresh or caching needed.

## License

MIT
