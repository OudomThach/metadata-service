"""Batch OCR DAG — submit files to the jobs-adapter, poll to completion, then
upsert results into the metadata service.

Pipeline (the traceability spine):
    upload -> job_id -> poll progress -> fetch JSONL results
           -> upsert records with pipeline.run_id=<job_id>
           -> every record traceable back to its source job

Requires (Airflow connections):
  - `jobs_adapter` (HTTP): host = the funnel/nginx base, e.g.
    https://apt-server-desktop.tail806605.ts.net
  - `metadata_service` (HTTP): same base (records API is open — no key needed)

Tune SCHEDULE / input list per deployment.
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.utils.dates import days_ago

DEFAULT_ARGS = {"retries": 2, "retry_delay": 30}

JOBS_BASE = "{{ conn.jobs_adapter.host }}"
META_BASE = "{{ conn.metadata_service.host }}"


def _submit_and_poll(job_files: list[str], **context) -> str:
    hook = HttpHook(method="POST", http_conn_id="jobs_adapter")
    resp = hook.run(
        endpoint=f"{JOBS_BASE}/v1/api-jobs/jobs",
        data=json.dumps({"files": job_files}),
        headers={"Content-Type": "application/json"},
    )
    job = resp.json()
    job_id = job["job_id"]
    context["ti"].xcom_push(key="job_id", value=job_id)

    poll = HttpHook(method="GET", http_conn_id="jobs_adapter")
    while True:
        status = poll.run(endpoint=f"{JOBS_BASE}/v1/api-jobs/jobs/{job_id}").json()
        if status["status"] in ("done", "failed", "cancelled"):
            return status
        time.sleep(10)


def _ingest_results(job_id: str, **context) -> int:
    """Fetch JSONL results and upsert into metadata (idempotent: skip dupes)."""
    hook = HttpHook(method="GET", http_conn_id="jobs_adapter")
    resp = hook.run(
        endpoint=f"{JOBS_BASE}/v1/api-jobs/jobs/{job_id}/result",
        headers={"Accept": "application/x-ndjson"},
    )
    ingest = HttpHook(method="POST", http_conn_id="metadata_service")
    created = 0
    for line in resp.text.splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        doc_id = re.sub(r"[^A-Za-z0-9_-]", "-", str(item.get("filename")))
        payload = {
            "id": f"doc-{doc_id}",
            "type": "document",
            "source": {
                "document_id": item.get("filename"),
                "filename": item.get("filename"),
                "model": "surya-vllm-v2",
                "source_system": "airflow",
            },
            "pipeline": {"run_id": job_id, "version": "1.0.0"},
            "data": item,
        }
        r = ingest.run(
            endpoint=f"{META_BASE}/api-meta/api/v1/records",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            extra_options={"params": {"on_duplicate": "skip"}},
        )
        if r.status_code == 201:
            created += 1
    return created


with DAG(
    dag_id="romdoul_ocr_batch",
    default_args=DEFAULT_ARGS,
    description="Batch OCR via jobs-adapter, results upserted to metadata",
    schedule_interval=None,  # trigger manually or from a sensor
    start_date=days_ago(1),
    catchup=False,
    tags=["romdoul", "ocr"],
) as dag:

    files = Variable.get("romdoul_batch_files", deserialize_json=True, default_var=[])

    submit = PythonOperator(
        task_id="submit_and_poll",
        python_callable=_submit_and_poll,
        op_kwargs={"job_files": files},
    )
    ingest = PythonOperator(
        task_id="ingest_results",
        python_callable=_ingest_results,
        op_kwargs={"job_id": "{{ ti.xcom_pull(task_ids='submit_and_poll', key='job_id') }}"},
    )

    submit >> ingest
