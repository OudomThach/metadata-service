from conftest import sample_record


async def test_batch_creates_all(auth_client):
    payloads = [sample_record(id=f"batch-{i:03d}") for i in range(3)]
    r = await auth_client.post("/api/v1/records/batch", json={"items": payloads})
    assert r.status_code == 200
    body = r.json()
    assert body["created"] == 3
    assert body["failed"] == 0
    assert all(item["ok"] for item in body["results"])
    assert len(body["results"]) == 3


async def test_batch_partial_failure_is_isolated(auth_client):
    payloads = [
        sample_record(id="batch-ok-1"),
        sample_record(id="batch-ok-2"),
        sample_record(audit={"status": "weird"}),  # invalid → item-level error
    ]
    r = await auth_client.post("/api/v1/records/batch", json={"items": payloads})
    assert r.status_code == 200
    body = r.json()
    assert body["created"] == 2
    assert body["failed"] == 1
    errors = [item for item in body["results"] if not item["ok"]]
    assert len(errors) == 1
    assert errors[0]["error"]["code"] == "invalid_status"

    r = await auth_client.get("/api/v1/records", params={"q": "INV-2201"})
    assert r.json()["total"] == 2


async def test_batch_rejects_too_many_items(auth_client):
    payloads = [sample_record(id=f"too-{i:04d}") for i in range(501)]
    r = await auth_client.post("/api/v1/records/batch", json={"items": payloads})
    assert r.status_code == 422


async def test_duplicate_skip_is_idempotent(auth_client):
    payload = sample_record()
    assert (await auth_client.post("/api/v1/records", json=payload)).status_code == 201
    r = await auth_client.post("/api/v1/records", json=payload, params={"on_duplicate": "skip"})
    assert r.status_code == 200
    assert r.json()["id"] == "rec-0001"


async def test_duplicate_replace_updates_record(auth_client):
    await auth_client.post("/api/v1/records", json=sample_record())
    payload = sample_record(data={"order_no": "INV-REPLACED", "amount": 999})
    r = await auth_client.post("/api/v1/records", json=payload, params={"on_duplicate": "replace"})
    assert r.status_code == 200
    body = r.json()
    assert body["data"]["order_no"] == "INV-REPLACED"
    assert body["edit_count"] >= 1


async def test_duplicate_error_is_default(auth_client):
    await auth_client.post("/api/v1/records", json=sample_record())
    r = await auth_client.post("/api/v1/records", json=sample_record())
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "duplicate_id"
