# Metadata Service — Integration Guide

How to push data into the metadata service and pull it back out, aimed at data
engineers wiring it into Airflow, dbt, or plain scripts, and analysts who need
clean exports.

Base URL: `https://<host>/api-meta` (behind the Romdoul nginx) or
`http://localhost:8095/api` (direct). All timestamps are ISO-8601 UTC.

## Auth

| Consumer | Mechanism |
|---|---|
| Machine / pipeline | **No key needed** — the records API (read/write/export/stats) is open by design |
| Role-gated ops | Present `X-API-Key` or a portal session token to get admin/editor role checks |
| Admin surface | Portal login (`/auth/login` → `X-Session-Token`), `/settings`, `/audit`, `/webhooks` are admin-only |

> **Before exposing this service to the public internet:** review the open
> API decision — reads/exports are intentionally keyless (analysts/DEs), but
> if you want authenticated access, re-enable `require_auth` on the record
> routers, add server-side rate limiting (429 + `Retry-After`), and rotate
> keys. The README's "rate-limited at nginx" claim is only true if nginx
> actually fronts the deployment.

## Error format

All endpoints (except `POST /auth/*` on validation failures) return:

```json
{ "error": { "code": "duplicate_id", "message": "record rec-x already exists" } }
```

Codes: `validation_error`, `not_found`, `duplicate_id`, `invalid_status`,
`invalid_credentials`, `forbidden`, `http_error`.

## Ingest — one record

```bash
curl -X POST http://localhost:8095/api/v1/records \
  -H "Content-Type: application/json" \
  -d '{
    "id": "rec-0001",                          # optional; idempotency key
    "type": "invoice",
    "source": {"document_id": "doc_1", "filename": "scan.pdf", "page": 1, "model": "surya-vllm-v2"},
    "pipeline": {"run_id": "run_1", "batch_id": "batch_1", "version": "1.2.0"},
    "business": {"date": "2026-08-01", "tags": ["import"], "domain": "logistics"},
    "data": {"order_no": "INV-2201", "amount": 1500}
  }'
```

### Duplicate handling (`on_duplicate`)

| Mode | Behavior |
|---|---|
| `error` (default) | `409 duplicate_id` |
| `skip` | returns the existing record, `200` |
| `replace` | overwrites data/envelope, bumps `edit_count`, `200` |

**Airflow retry pattern:** pass `?on_duplicate=skip` so a re-run of a failed
DAG is safe — no 409s, no double writes.

## Ingest — batch (up to 500 items)

```bash
curl -X POST http://localhost:8095/api/v1/records/batch \
  -H "Content-Type: application/json" \
  -d '{"items": [ {record...}, {record...} ]}'
```

Response: per-item isolation — one bad item never rolls back the others.

```json
{
  "created": 2, "updated": 0, "skipped": 0, "failed": 1,
  "results": [
    {"id": "rec-0001", "ok": true},
    {"id": "rec-0002", "ok": true},
    {"id": null, "ok": false, "error": {"code": "invalid_status", "message": "..."}}
  ]
}
```

## Read / query

```
GET /api/v1/records?type=invoice&domain=logistics&status=raw&tag=import
                   &business_from=2026-08-01&business_to=2026-08-31
                   &created_from=2026-08-01T00:00:00Z&created_to=...
                   &edited_from=2026-08-01T00:00:00Z&edited_to=...
                   &q=INV
                   &page=1&page_size=200&sort=created_at:desc
```

- `q` searches record `data` + `envelope` JSON (text match)
- `created_from/to` = new-record window; `edited_from/to` = changed-record
  window (CDC sync: combine both for "everything new or updated since X")
- sortable columns: `created_at`, `business_date`, `edited_at`, `type`, `status`
- `page_size` max 200

## Export (analysts + pipelines)

| Format | Endpoint | Use case |
|---|---|---|
| CSV (UTF-8 BOM) | `GET /api/v1/export?format=csv` | Excel / spreadsheets |
| JSONL (streamed) | `GET /api/v1/export?format=jsonl` | pipelines, `jq`, big pulls |
| Parquet (streamed) | `GET /api/v1/export?format=parquet` | data scientists / warehouses |
| JSON (array) | `GET /api/v1/export?format=json` | small payloads |

All support the same filters as `/records` (incl. `edited_from/to`). CSV,
JSONL and Parquet **stream from the database** — memory stays flat at any row
count.

**Incremental sync recipe (Airflow daily):**

```bash
curl "http://localhost:8095/api/v1/export?format=jsonl&created_from=$(date -u -d yesterday +%F)&edited_from=$(date -u -d yesterday +%F)" \
  -H "X-API-Key: $KEY" > /tmp/records-$(date +%F).jsonl
```

## Traceability

Every record is traceable end-to-end (source job → ingest → edits → verify →
dataset → export) via the open `GET /api/v1/records/{id}/trace` endpoint and
the immutable audit chain. See [`TRACEABILITY.md`](TRACEABILITY.md).

## Python SDK

```bash
pip install ./sdk
```

Typed client for every endpoint (records, batch, export, datasets, trace,
webhooks). See [`sdk/README.md`](../sdk/README.md). Airflow DAG templates
using it live in [`dags/`](../dags/).

## Stats & metadata

```
GET /api/v1/stats   # totals by status/type/domain/model, daily trend
GET /api/v1/meta    # distinct types + domains (filter dropdowns)
GET /health         # liveness + DB check
```

## Webhooks (event-driven pipelines)

Admin-managed: `POST /api/v1/webhooks` with `{"url": "...", "events": ["create","update","delete"]}`.
Fired fire-and-forget per record event with 5s timeout. Only public http(s)
targets are allowed (SSRF guard).

## Error-handling guidance for pipelines

- `409` → use `on_duplicate=skip|replace` instead of erroring
- `401` → bad/missing session token or key on a role-gated endpoint
- `422` → validation error, inspect `error.fields`
- `5xx` → retry with exponential backoff (the service is stateless per request)

## Airflow example (SimpleHttpOperator)

```python
from airflow.providers.http.operators.http import SimpleHttpOperator

ingest = SimpleHttpOperator(
    task_id="ingest_records",
    http_conn_id="metadata_service",          # host: http://localhost:8095
    endpoint="/api/v1/records/batch",
    method="POST",
    headers={"X-API-Key": "{{ conn.metadata_service.extra_dejson.api_key }}"},
    data=json.dumps({"items": records}),
    response_check=lambda r: r.json()["failed"] == 0,
    retries=3,
)
```
