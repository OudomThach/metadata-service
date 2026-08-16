"""Incremental records sync DAG — pull records changed since the last run into
a warehouse (Parquet/CSV/JSONL).

Watermarking: the last `edited_at` (or `created_at` if nothing was edited) is
stored in an Airflow Variable, so each run pulls exactly the delta since the
previous run. Combined created/edited windows make this a CDC-style sync:
new records via created_from, updated records via edited_from.

Requires an HTTP connection `metadata_service` (host = funnel/nginx base).
The records API is open — no keys needed.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.utils.dates import days_ago

META_BASE = "{{ conn.metadata_service.host }}"
WATERMARK_KEY = "romdoul_sync_watermark"
EXPORT_DIR = "/tmp/romdoul_sync"


def _last_watermark() -> str:
    return Variable.get(WATERMARK_KEY, default_var="2000-01-01T00:00:00Z")


def _pull_delta(**context) -> str:
    """Export records edited/created since the watermark as Parquet."""
    since = _last_watermark()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    hook = HttpHook(method="GET", http_conn_id="metadata_service")
    resp = hook.run(
        endpoint=f"{META_BASE}/api-meta/api/v1/export",
        headers={"Accept": "application/vnd.apache.parquet"},
        extra_options={
            "params": {
                "format": "parquet",
                "edited_from": since,
                "created_from": since,
                "edited_to": now,
                "created_to": now,
            }
        },
    )
    path = f"{EXPORT_DIR}/records-{context['ds']}.parquet"
    with open(path, "wb") as f:
        f.write(resp.content)
    context["ti"].xcom_push(key="watermark", value=now)
    return path


def _advance_watermark(**context) -> None:
    Variable.set(WATERMARK_KEY, context["ti"].xcom_pull(task_ids="pull_delta", key="watermark"))


with DAG(
    dag_id="romdoul_sync_records",
    default_args={"retries": 3, "retry_delay": 60},
    description="Incremental CDC-style sync of records to Parquet",
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
    tags=["romdoul", "sync"],
) as dag:

    pull = PythonOperator(task_id="pull_delta", python_callable=_pull_delta)
    advance = PythonOperator(task_id="advance_watermark", python_callable=_advance_watermark)

    pull >> advance
