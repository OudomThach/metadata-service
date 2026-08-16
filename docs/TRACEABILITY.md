# Traceability — "where did this come from, who touched it, when"

Every record in the metadata service is traceable end-to-end: from the source
upload/job through ingestion, edits, verification, promotion to a dataset,
and export. Public by default — the records API is open and `/trace` requires
no credentials.

## The chain

```
Upload / batch job (jobs-adapter)
   │  pipeline.run_id = <job_id>   ← stamped at ingest (capture-ocr / records)
   ▼
Record created (status=raw)
   │  source: document_id, filename, page, model, source_system
   │  pipeline: run_id, batch_id, version
   ▼
Edits (status → edited)      ── audit event "update" (actor, at, snapshot)
   ▼
Verification (status → verified) ── audit event "update" + status_verified_at
   │
   ├── auto-promote → Dataset (draft → published → archived)
   ▼
Export (CSV / JSONL / Parquet) ── carries source_*/pipeline_* lineage columns
```

## How to trace

### API — `GET /api/v1/records/{id}/trace` (open)

```bash
curl https://<host>/api-meta/api/v1/records/rec-0001/trace
```

Returns:

| Field | Meaning |
|---|---|
| `record` | Current record state |
| `lineage.source` | Where the document came from (filename, model, system, page) |
| `lineage.pipeline` | run_id / batch_id / version of the producing pipeline |
| `lineage.business` | Domain metadata at ingest |
| `lineage.record` | Validation status/warnings + ingest timestamp |
| `lineage.status_verified_at` | When verification happened |
| `audit[]` | Immutable per-record history: create → every update → delete, each with actor + snapshot |
| `dataset` | The promoted dataset (if any) |

### Portal — Record detail → "Lineage & audit" tab

Shows the same chain visually: provenance, pipeline job id, edit history with
actors and timestamps, and the promoted dataset.

### Export — lineage columns

CSV/Parquet exports already include `source_filename`, `source_model`,
`source_system`, `source_page`, `pipeline_run_id`, `pipeline_batch_id`,
`created_by`, `edited_by`, `edit_count`, `validation_status` — so a warehouse
copy stays fully traceable.

## Audit guarantees

- **Immutable**: every change appends an `AuditEvent` row; the record's
  snapshot is stored with the event. No in-place mutation of history.
- **Attributed**: `user:<name>` (portal), `key:<key>` (API key), or
  `system:<who>` (open API / pipelines) — plus the optional
  `X-Edited-By: user:<name>` header for pipeline attribution.
- **Counted**: `edit_count` increments on every write, visible in the record
  and exports.
- **Deleted records**: the audit trail is kept (`ondelete=CASCADE` applies to
  the record row; export the trace before deleting if you need the chain).

## Lineage stamping rules

| Ingest path | What gets stamped |
|---|---|
| `POST /records` + `POST /records/batch` | `pipeline` (run_id/batch_id/version) + `source` from the payload — callers control it |
| `POST /capture-ocr` | `pipeline` + `source` optional fields (adapters send `run_id=<job_id>`) |
| Airflow DAGs (see `dags/`) | `pipeline.run_id=<job_id>` on every upsert |

## Worked example

```bash
# 1. a batch job produces records with run_id=job_42
curl "https://<host>/api-meta/api/v1/records?q=job_42" | jq '.items[].id'

# 2. full trace of one record
curl "https://<host>/api-meta/api/v1/records/rec-x/trace" | jq '.audit[] | {action, actor, at}'

# 3. incremental sync since a point in time (CDC)
curl "https://<host>/api-meta/api/v1/export?format=parquet&edited_from=2026-08-01T00:00:00Z" \
  -o changed.parquet
```
