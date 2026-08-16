"""Published datasets snapshot DAG — export all published datasets + stats to
Parquet/JSON so analysts and downstream systems always have a fresh copy.

Requires an HTTP connection `metadata_service` (host = funnel/nginx base).
Datasets reads are public (published only); stats/meta are open.
"""

from __future__ import annotations

import json
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.utils.dates import days_ago

META_BASE = "{{ conn.metadata_service.host }}"
SNAPSHOT_DIR = "/tmp/romdoul_sync"


def _export_datasets(**context) -> str:
    hook = HttpHook(method="GET", http_conn_id="metadata_service")
    resp = hook.run(
        endpoint=f"{META_BASE}/api-meta/api/v1/datasets",
        extra_options={"params": {"public": "true", "page_size": "200"}},
    )
    path = f"{SNAPSHOT_DIR}/datasets-{context['ds']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(resp.json(), f, ensure_ascii=False)
    return path


def _export_stats(**context) -> str:
    hook = HttpHook(method="GET", http_conn_id="metadata_service")
    resp = hook.run(endpoint=f"{META_BASE}/api-meta/api/v1/stats")
    path = f"{SNAPSHOT_DIR}/stats-{context['ds']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(resp.json(), f, ensure_ascii=False)
    return path


with DAG(
    dag_id="romdoul_export_datasets",
    default_args={"retries": 2, "retry_delay": 60},
    description="Snapshot published datasets + stats",
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
    tags=["romdoul", "datasets"],
) as dag:

    datasets = PythonOperator(task_id="export_datasets", python_callable=_export_datasets)
    stats = PythonOperator(task_id="export_stats", python_callable=_export_stats)

    datasets
    stats
