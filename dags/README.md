# Airflow DAGs

Three ready-to-run DAGs that automate the full Romdoul loop. Copy the `dags/`
folder into your Airflow `dags/` directory.

## Connections required

| Conn id | Type | Host |
|---|---|---|
| `jobs_adapter` | HTTP | funnel/nginx base, e.g. `https://apt-server-desktop.tail806605.ts.net` |
| `metadata_service` | HTTP | same base |

The records API is open — no keys needed for reads/writes/exports.

## DAGs

| DAG | What it does | Schedule |
|---|---|---|
| `romdoul_ocr_batch` | Submit files to jobs-adapter → poll → fetch JSONL → upsert records with `pipeline.run_id=<job_id>` (traceable) | manual (or sensor) |
| `romdoul_sync_records` | CDC-style incremental pull (`edited_from`/`created_from` since watermark) → Parquet to `/tmp/romdoul_sync/` | daily |
| `romdoul_export_datasets` | Snapshot published datasets + stats → JSON | daily |

## Watermark

`romdoul_sync_records` stores the last sync time in the Airflow Variable
`romdoul_sync_watermark` — each run pulls exactly the delta. Reset it to
`2000-01-01T00:00:00Z` to re-pull everything.

## Webhook → DAG trigger

To start a DAG from a metadata webhook (e.g. on record create), register a
webhook whose URL is Airflow's REST API:

```bash
# register (admin session required):
curl -X POST https://<host>/api-meta/api/v1/webhooks \
  -H "X-Session-Token: <token>" \
  -d '{"url": "https://<airflow>/api/v1/dags/romdoul_sync_records/dagRuns",
       "events": ["create"]}'
```

Airflow receives the metadata event payload as the dagRun `conf` (enable the
`Airflow API` auth or put the webhook URL behind your Airflow auth).
