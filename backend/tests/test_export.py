import csv
import io


async def _seed(auth_client):
    for i in range(3):
        p = {
            "id": f"exp-{i:04d}",
            "type": "invoice" if i % 2 == 0 else "label",
            "business": {"date": "2026-08-01", "tags": ["t"], "domain": "logistics"},
            "data": {"n": i},
        }
        await auth_client.post("/api/v1/records", json=p)


async def test_export_json(auth_client):
    await _seed(auth_client)
    r = await auth_client.get("/api/v1/export", params={"format": "json"})
    assert r.status_code == 200
    assert len(r.json()) == 3


async def test_export_csv_flattened(auth_client):
    await _seed(auth_client)
    r = await auth_client.get("/api/v1/export", params={"format": "csv", "type": "invoice"})
    assert r.status_code == 200
    text = r.text.lstrip("\ufeff")  # BOM is intentional (Excel-safe)
    rows = list(csv.reader(io.StringIO(text)))
    assert len(rows) == 3  # header + 2 invoice rows
    assert rows[0][0] == "id"
    assert rows[1][1] == "invoice"


async def test_export_csv_respects_filters(auth_client):
    await _seed(auth_client)
    r = await auth_client.get("/api/v1/export", params={"format": "csv", "status": "raw"})
    text = r.text.lstrip("\ufeff")
    assert len(list(csv.reader(io.StringIO(text)))) == 4


async def test_export_jsonl_streams_rows(auth_client):
    await _seed(auth_client)
    r = await auth_client.get("/api/v1/export", params={"format": "jsonl"})
    assert r.status_code == 200
    lines = [ln for ln in r.text.strip().split("\n") if ln.strip()]
    assert len(lines) == 3
    assert lines[0].count('"id"') >= 1


async def test_export_jsonl_respects_filters(auth_client):
    await _seed(auth_client)
    r = await auth_client.get("/api/v1/export", params={"format": "jsonl", "type": "label"})
    lines = [ln for ln in r.text.strip().split("\n") if ln.strip()]
    assert len(lines) == 1
    assert '"label"' in lines[0]


async def test_stats_has_no_duplicate_keys(auth_client):
    await _seed(auth_client)
    r = await auth_client.get("/api/v1/stats")
    assert r.status_code == 200
    # JSON parsing keeps only the last duplicate key — assert the raw body
    # contains each top-level key exactly once.
    raw = r.text
    for key in (
        "total",
        "by_status",
        "by_type",
        "by_domain",
        "by_model",
        "edited",
        "verified",
        "coverage_avg",
        "per_day",
    ):
        assert raw.count(f'"{key}"') == 1, f"duplicate or missing key: {key}"
    body = r.json()
    assert "by_domain" in body
    assert "by_type" in body
