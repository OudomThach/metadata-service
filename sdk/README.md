# metadata-service Python SDK

Generated client for the metadata-service API (`openapi-python-client`).
Typed models + async/httpx client for records, batch ingest, export
(CSV/JSONL/Parquet), stats, datasets, traceability and admin endpoints.

## Install

```bash
pip install ./sdk
# or from the repo root:
pip install -e ./sdk
```

## Quick start

```python
from sdk.client import Client
from sdk.api.records import create_record_api_v1_records_post
from sdk.api.export import export_api_v1_export_get

client = Client(base_url="https://romdoulocr.netlify.app/api-meta/api/v1")

# Ingest (records API is open — no keys needed)
create_record_api_v1_records_post.sync(
    client=client,
    body={"id": "rec-1", "type": "invoice", "data": {"order_no": "INV-1"}},
)
```

## Regenerate

```bash
# after backend changes, from backend/:
python -m openapi_python_client generate --path openapi.json --output-path ../sdk --meta none
```

## What's here

- `sdk/client.py` — httpx-based `Client` (sync/async)
- `sdk/api/` — one module per route group: records (incl. batch + on_duplicate),
  export (csv/json/jsonl/parquet + created/edited windows), datasets (+ file
  download), stats, meta, trace, webhooks, admin, auth
- `sdk/models/` — typed request/response models
