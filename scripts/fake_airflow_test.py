"""
FAKE AIRFLOW INTEGRATION TEST
=============================
Runs the REAL Airflow DAG files from dags/ against the REAL FastAPI app
(in-process via ASGITransport), with a stubbed Airflow runtime:

  - airflow.DAG / days_ago / Variable / PythonOperator / TaskInstance -> stubs
  - HttpHook (airflow.providers.http) -> httpx ASGITransport against the app;
    jobs-adapter endpoints (/api-jobs/...) are FAKED (no GPU/engines)

Proves exactly what Airflow would do in production:
  1. dag_sync_records: CDC Parquet pull with watermark advance; second run is
     incremental (0 rows).
  2. dag_export_datasets: published-datasets + stats JSON snapshots.
  3. dag_ocr_batch._ingest_results: fetches JSONL from a (fake) job and upserts
     records carrying pipeline.run_id=<job_id> - traceable and idempotent.

Run from the repo root:
    $env:PYTHONPATH = "backend"; python scripts/fake_airflow_test.py
"""

import asyncio
import importlib.util
import json
import os
import sys
import threading
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BACKEND = REPO / "backend"
DAGS = REPO / "dags"

os.environ["METADATA_DATABASE_URL"] = "sqlite+aiosqlite:///./airflow_test.db"
os.environ["METADATA_ADMIN_PASSWORD"] = "af-test-password-123"
os.environ["METADATA_API_KEYS"] = "af-machine-key"

DB_FILE = Path.cwd() / "airflow_test.db"  # URL is CWD-relative
if DB_FILE.exists():
    DB_FILE.unlink()

sys.path.insert(0, str(BACKEND))

import app.main
import app.models
from app.db import Base, engine
from app.main import app
from app.security import seed_admin
from httpx import ASGITransport, AsyncClient

# --------------------------------------------------------------------------- #
# single long-lived event loop (SQLAlchemy aiosqlite pool stays on one loop)
# --------------------------------------------------------------------------- #
_loop = asyncio.new_event_loop()
threading.Thread(target=_loop.run_forever, daemon=True).start()


class _Resp:
    def __init__(self, status_code: int, content: bytes, headers: dict):
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self.text = content.decode("utf-8", "replace")

    def json(self):
        return json.loads(self.text)


def api(method: str, path: str, *, json_body=None, data=None, headers=None, params=None) -> _Resp:
    """Synchronous API call into the app, dispatched on the shared loop."""

    async def _do():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            r = await client.request(
                method, path, json=json_body, content=data, headers=headers, params=params
            )
            return _Resp(r.status_code, r.content, dict(r.headers))

    return asyncio.run_coroutine_threadsafe(_do(), _loop).result()


# --------------------------------------------------------------------------- #
# Airflow runtime stubs
# --------------------------------------------------------------------------- #
class _DAG:
    def __init__(self, *a, **kw):
        self.dag_id = kw.get("dag_id", "test")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _PythonOperator:
    def __init__(self, task_id, python_callable, op_kwargs=None, **kw):
        self.task_id = task_id
        self.python_callable = python_callable
        self.op_kwargs = op_kwargs or {}
        self.upstream: list[_PythonOperator] = []

    def __rshift__(self, other):
        other.upstream.append(self)
        return other


class _Variable:
    _store: dict[str, str] = {}  # noqa: RUF012  (test stub, shared by design)

    @classmethod
    def set(cls, key, value):
        cls._store[key] = str(value)

    @classmethod
    def get(cls, key, default_var=None, deserialize_json=False):
        val = cls._store.get(key)
        if val is None:
            return default_var
        return json.loads(val) if deserialize_json else val


class _TI:
    def __init__(self):
        self._xcom: dict[str, object] = {}

    def xcom_push(self, key, value):
        self._xcom[key] = value

    def xcom_pull(self, task_ids=None, key=None):
        return self._xcom.get(key)


class _HttpHook:
    """Airflow HttpHook stub -> real app via ASGITransport.
    Endpoints containing /api-jobs/ are FAKED (no OCR engines): POST /jobs
    returns job_42, GET /jobs/{id} returns done, GET /jobs/{id}/result
    returns canned JSONL. Everything else hits the real API."""

    def __init__(self, method="GET", http_conn_id=None):
        self.method = method
        self.http_conn_id = http_conn_id

    def run(self, endpoint=None, data=None, headers=None, extra_options=None, **kw):
        if "/api-jobs" in endpoint:
            return self._fake_jobs(endpoint, data)
        path = endpoint.split("/api-meta", 1)[-1]  # strip conn host + prefix
        params = (extra_options or {}).get("params") or {}
        return api(self.method, path, data=data, headers=headers, params=params)

    def _fake_jobs(self, endpoint: str, data):
        if endpoint.endswith("/result"):
            payload = [
                {"filename": "doc_a.pdf", "full_text": "Invoice line one", "num_pages": 1},
                {"filename": "doc_b.pdf", "full_text": "Invoice line two", "num_pages": 2},
            ]
            body = "\n".join(json.dumps(p) for p in payload).encode()
            return _Resp(200, body, {"content-type": "application/x-ndjson"})
        if endpoint.endswith("/jobs"):
            return _Resp(200, b'{"job_id": "job_42"}', {})
        return _Resp(200, b'{"job_id": "job_42", "status": "done"}', {})


AIRFLOW = types.ModuleType("airflow")
AIRFLOW.__path__ = []
AIRFLOW.DAG = _DAG
AIRFLOW.models = types.ModuleType("airflow.models")
AIRFLOW.models.Variable = _Variable
AIRFLOW.operators = types.ModuleType("airflow.operators")
AIRFLOW.operators.python = types.ModuleType("airflow.operators.python")
AIRFLOW.operators.python.PythonOperator = _PythonOperator
AIRFLOW.providers = types.ModuleType("airflow.providers")
AIRFLOW.providers.http = types.ModuleType("airflow.providers.http")
AIRFLOW.providers.http.hooks = types.ModuleType("airflow.providers.http.hooks")
AIRFLOW.providers.http.hooks.http = types.ModuleType("airflow.providers.http.hooks.http")
AIRFLOW.providers.http.hooks.http.HttpHook = _HttpHook
AIRFLOW.utils = types.ModuleType("airflow.utils")
AIRFLOW.utils.dates = types.ModuleType("airflow.utils.dates")
AIRFLOW.utils.dates.days_ago = lambda n: "2026-08-15"
for name, mod in [
    ("airflow", AIRFLOW),
    ("airflow.models", AIRFLOW.models),
    ("airflow.operators", AIRFLOW.operators),
    ("airflow.operators.python", AIRFLOW.operators.python),
    ("airflow.providers", AIRFLOW.providers),
    ("airflow.providers.http", AIRFLOW.providers.http),
    ("airflow.providers.http.hooks", AIRFLOW.providers.http.hooks),
    ("airflow.providers.http.hooks.http", AIRFLOW.providers.http.hooks.http),
    ("airflow.utils", AIRFLOW.utils),
    ("airflow.utils.dates", AIRFLOW.utils.dates),
]:
    sys.modules[name] = mod

# --------------------------------------------------------------------------- #
# load the REAL dag files
# --------------------------------------------------------------------------- #


def load_dag(name: str) -> dict:
    spec = importlib.util.spec_from_file_location(name, DAGS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.__dict__


# --------------------------------------------------------------------------- #
# test flow
# --------------------------------------------------------------------------- #
def main() -> None:
    ok = True
    asyncio.run_coroutine_threadsafe(_bootstrap(), _loop).result()

    export_dir = Path(os.environ["TEMP"]) / "romdoul_sync"
    export_dir.mkdir(exist_ok=True)

    # -- seed data through the REAL API ------------------------------------
    print("-- seed 2 records (source=pipeline seed-run) --")
    for rid, typ in [("af-1", "invoice"), ("af-2", "label")]:
        r = api(
            "POST",
            "/api/v1/records",
            json_body={
                "id": rid,
                "type": typ,
                "source": {"model": "surya-vllm-v2", "source_system": "airflow-test"},
                "pipeline": {"run_id": "seed-run"},
                "data": {"n": 1},
            },
        )
        assert r.status_code == 201, r.text
        ok &= r.status_code == 201

    print("-- seed 1 published dataset (admin session) --")
    token = api(
        "POST",
        "/api/v1/auth/login",
        json_body={"username": "admin", "password": "af-test-password-123"},
    ).json()["token"]
    ds = api(
        "POST",
        "/api/v1/datasets",
        json_body={
            "name": "CPI 2020 Yearbook",
            "description": "Consumer price index tables",
            "file_name": "cpi_2020.csv",
            "file_type": "text/csv",
            "file_base64": "cmVwb3J0X3llYXIsc2NvcGUsdGV4dAoyMDIwLGNwaS15ZWFyYm9vayxJbmZsYXRpb24gNC42JQo=",
        },
        headers={"X-Session-Token": token},
    ).json()
    pub = api(
        "POST", f"/api/v1/datasets/{ds['id']}/publish", headers={"X-Session-Token": token}
    ).json()
    print(f"dataset {ds['id'][:8]} status={pub['status']}")
    ok &= pub["status"] == "published"

    # -- 1. dag_sync_records: first run ------------------------------------
    print("-- dag_sync_records: run 1 --")
    sync = load_dag("dag_sync_records")
    sync["EXPORT_DIR"] = str(export_dir)
    ti1 = _TI()
    path1 = sync["_pull_delta"](ti=ti1, ds="2026-08-16")
    wm = ti1.xcom_pull(task_ids="pull_delta", key="watermark")
    sync["_advance_watermark"](ti=ti1)
    stored = _Variable.get("romdoul_sync_watermark")
    print(f"parquet: {Path(path1).name} exists={Path(path1).exists()}")
    print(f"watermark pushed={wm is not None} stored={stored == wm}")
    ok &= Path(path1).exists() and wm is not None and stored == wm

    rows1 = _parquet_rows(path1)
    print(f"run 1 rows: {rows1}")
    ok &= rows1 == 2

    # -- 2. dag_sync_records: second run (incremental) ---------------------
    print("-- dag_sync_records: run 2 (expect 0 rows) --")
    ti2 = _TI()
    path2 = sync["_pull_delta"](ti=ti2, ds="2026-08-17")
    rows2 = _parquet_rows(path2)
    print(f"run 2 rows: {rows2}")
    ok &= rows2 == 0

    # -- 3. dag_export_datasets --------------------------------------------
    print("-- dag_export_datasets --")
    exp = load_dag("dag_export_datasets")
    exp["SNAPSHOT_DIR"] = str(export_dir)
    dsp = exp["_export_datasets"](ds="2026-08-16")
    stp = exp["_export_stats"](ds="2026-08-16")
    ds_json = json.loads(Path(dsp).read_text(encoding="utf-8"))
    st_json = json.loads(Path(stp).read_text(encoding="utf-8"))
    print(f"datasets snapshot total={ds_json.get('total')} stats total={st_json.get('total')}")
    ok &= ds_json.get("total") == 1 and st_json.get("total") == 2

    # -- 4. dag_ocr_batch._ingest_results (fake jobs-adapter) --------------
    print("-- dag_ocr_batch._ingest_results (job_42, fake jobs-adapter) --")
    batch = load_dag("dag_ocr_batch")
    created = batch["_ingest_results"](job_id="job_42")
    print(f"records created: {created}")
    ok &= created == 2

    # rerun -> idempotent (on_duplicate=skip + deterministic doc ids)
    created2 = batch["_ingest_results"](job_id="job_42")
    print(f"rerun created: {created2} (expect 0)")
    ok &= created2 == 0

    # traceability: records carry pipeline.run_id=job_42
    items = api("GET", "/api/v1/records", params={"page_size": 50}).json()["items"]
    job_recs = [
        i
        for i in items
        if (i.get("envelope") or {}).get("pipeline", {}).get("run_id") == "job_42"
    ]
    print(f"records with pipeline.run_id=job_42: {len(job_recs)}")
    ok &= len(job_recs) == 2

    print()
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


async def _bootstrap() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_admin()  # lifespan equivalent (ASGITransport skips lifespan)


def _parquet_rows(path: str) -> int:
    try:
        import pyarrow.parquet as pq

        return pq.read_table(path).num_rows
    except ImportError:
        head = Path(path).read_bytes()[:4]
        return -1 if head != b"PAR1" else 0  # magic ok; row count via pyarrow unavailable


if __name__ == "__main__":
    main()
