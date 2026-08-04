import csv
import io


async def _seed(client):
    for i in range(3):
        p = {
            "id": f"exp-{i:04d}",
            "type": "invoice" if i % 2 == 0 else "label",
            "business": {"date": "2026-08-01", "tags": ["t"], "domain": "logistics"},
            "data": {"n": i},
        }
        await client.post("/api/v1/records", json=p)


async def test_export_json(client):
    await _seed(client)
    r = await client.get("/api/v1/export", params={"format": "json"})
    assert r.status_code == 200
    assert len(r.json()) == 3


async def test_export_csv_flattened(client):
    await _seed(client)
    r = await client.get("/api/v1/export", params={"format": "csv", "type": "invoice"})
    assert r.status_code == 200
    rows = list(csv.reader(io.StringIO(r.text)))
    assert len(rows) == 3  # header + 2 invoice rows
    assert rows[0][0] == "id"
    assert rows[1][1] == "invoice"


async def test_export_csv_respects_filters(client):
    await _seed(client)
    r = await client.get("/api/v1/export", params={"format": "csv", "status": "raw"})
    assert len(list(csv.reader(io.StringIO(r.text)))) == 4
