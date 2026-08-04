async def test_stats_aggregates(client):
    for i in range(4):
        p = {"id": f"st-{i:04d}", "type": "invoice" if i % 2 == 0 else "label",
             "business": {"domain": "logistics", "tags": ["t"], "coverage": 0.5 + i * 0.1},
             "data": {"n": i}}
        await client.post("/api/v1/records", json=p)
    await client.patch("/api/v1/records/st-0000", json={"data": {"n": 99}})
    await client.patch("/api/v1/records/st-0001", json={"status": "verified"})

    r = await client.get("/api/v1/stats")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 4
    assert body["by_type"] == {"invoice": 2, "label": 2}
    assert body["by_domain"] == {"logistics": 4}
    assert body["edited"] == 2
    assert body["verified"] == 1
    assert body["coverage_avg"] == 0.65


async def test_meta_lists_types_and_domains(client):
    await client.post("/api/v1/records", json={"id": "m-1", "type": "invoice",
                                               "business": {"domain": "logistics"}, "data": {}})
    r = await client.get("/api/v1/meta")
    assert r.json() == {"types": ["invoice"], "domains": ["logistics"]}


async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["db"] == "ok"
