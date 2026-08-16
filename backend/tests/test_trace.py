from conftest import sample_record


async def test_trace_returns_lineage_and_audit(auth_client):
    await auth_client.post(
        "/api/v1/records",
        json=sample_record(
            id="trace-1",
            source={"document_id": "doc_9", "filename": "scan.pdf", "model": "surya-vllm-v2", "source_system": "jobs"},
            pipeline={"run_id": "job_42", "batch_id": "batch_7", "version": "1.2.0"},
        ),
    )
    await auth_client.patch("/api/v1/records/trace-1", json={"data": {"order_no": "X"}})
    r = await auth_client.get("/api/v1/records/trace-1/trace")
    assert r.status_code == 200
    body = r.json()
    assert body["record"]["id"] == "trace-1"
    assert body["lineage"]["pipeline"]["run_id"] == "job_42"
    assert body["lineage"]["source"]["source_system"] == "jobs"
    actions = [e["action"] for e in body["audit"]]
    assert actions == ["create", "update"]


async def test_trace_not_found(auth_client):
    r = await auth_client.get("/api/v1/records/nope/trace")
    assert r.status_code == 404


async def test_capture_ocr_stamps_pipeline(client, monkeypatch):
    from app import config
    from app.security import seed_admin

    monkeypatch.setattr(config.settings, "admin_username", "admin")
    monkeypatch.setattr(config.settings, "admin_password", "admin-pass-123")
    await seed_admin()
    token = (await client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin-pass-123"})).json()[
        "token"
    ]
    r = await client.post(
        "/api/v1/capture-ocr",
        json={
            "document_name": "scan.pdf",
            "full_text": "hello",
            "pipeline": {"run_id": "job_99", "batch_id": "b1", "version": "2.0"},
            "source": {"document_id": "doc_1", "model": "surya-vllm-v2", "source_system": "jobs"},
        },
        headers={"X-Session-Token": token},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["envelope"]["pipeline"]["run_id"] == "job_99"
    assert body["source_system"] == "jobs"
    trace = (await client.get(f"/api/v1/records/{body['id']}/trace")).json()
    assert trace["lineage"]["pipeline"]["run_id"] == "job_99"


async def test_edited_from_filter(auth_client):
    await auth_client.post("/api/v1/records", json=sample_record(id="e-1"))
    await auth_client.patch("/api/v1/records/e-1", json={"data": {"n": 2}})

    r = await auth_client.get("/api/v1/records", params={"edited_from": "2100-01-01T00:00:00Z"})
    assert r.json()["total"] == 0

    r = await auth_client.get("/api/v1/records", params={"edited_from": "2000-01-01T00:00:00Z"})
    assert r.json()["total"] == 1
    assert r.json()["items"][0]["id"] == "e-1"


async def test_export_parquet(auth_client):
    await auth_client.post("/api/v1/records", json=sample_record())
    r = await auth_client.get("/api/v1/export", params={"format": "parquet"})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/vnd.apache.parquet")
    assert len(r.content) > 0
    # magic bytes PA R 1
    assert r.content[:4] == b"PAR1"


async def test_dataset_file_download(client, monkeypatch):
    from app import config
    from app.security import seed_admin

    monkeypatch.setattr(config.settings, "admin_username", "admin")
    monkeypatch.setattr(config.settings, "admin_password", "admin-pass-123")
    await seed_admin()
    token = (await client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin-pass-123"})).json()[
        "token"
    ]
    headers = {"X-Session-Token": token}

    import base64

    encoded = base64.b64encode(b"a,b\n1,2\n").decode()
    r = await client.post(
        "/api/v1/datasets",
        json={
            "name": "CPI 2020",
            "file_name": "cpi.csv",
            "file_type": "text/csv",
            "file_base64": encoded,
        },
        headers=headers,
    )
    assert r.status_code == 201
    ds_id = r.json()["id"]

    # draft -> blocked for public
    assert (await client.get(f"/api/v1/datasets/{ds_id}/file")).status_code == 403
    await client.post(f"/api/v1/datasets/{ds_id}/publish", headers=headers)
    r = await client.get(f"/api/v1/datasets/{ds_id}/file")
    assert r.status_code == 200
    assert r.content == b"a,b\n1,2\n"
    assert "attachment" in r.headers["content-disposition"]
