import pytest


async def test_seed_admin_fails_on_default_password(monkeypatch):
    from app import config
    from app.security import seed_admin

    monkeypatch.setattr(config.settings, "admin_password", "admin")
    with pytest.raises(RuntimeError):
        await seed_admin()


async def test_seed_admin_fails_on_empty_password(monkeypatch):
    from app import config
    from app.security import seed_admin

    monkeypatch.setattr(config.settings, "admin_password", "")
    with pytest.raises(RuntimeError):
        await seed_admin()


async def test_settings_list_requires_auth(client):
    r = await client.get("/api/v1/settings")
    assert r.status_code == 401


async def test_settings_list_requires_admin(client, monkeypatch):
    from app import config
    from app.security import seed_admin

    monkeypatch.setattr(config.settings, "admin_username", "admin")
    monkeypatch.setattr(config.settings, "admin_password", "admin-pass-123")
    await seed_admin()

    r = await client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin-pass-123"})
    admin_token = r.json()["token"]
    headers = {"X-Session-Token": admin_token}

    await client.post(
        "/api/v1/auth/users",
        json={"username": "dara", "password": "dara-pass-123", "role": "viewer"},
        headers=headers,
    )
    viewer_token = (
        await client.post("/api/v1/auth/login", json={"username": "dara", "password": "dara-pass-123"})
    ).json()["token"]

    assert (await client.get("/api/v1/settings", headers={"X-Session-Token": viewer_token})).status_code == 403
    assert (await client.get("/api/v1/settings", headers=headers)).status_code == 200


async def test_webhook_rejects_private_and_bad_urls(client, monkeypatch):
    from app import config
    from app.security import seed_admin

    monkeypatch.setattr(config.settings, "admin_username", "admin")
    monkeypatch.setattr(config.settings, "admin_password", "admin-pass-123")
    await seed_admin()
    token = (await client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin-pass-123"})).json()[
        "token"
    ]
    headers = {"X-Session-Token": token}

    assert (
        await client.post(
            "/api/v1/webhooks", json={"url": "http://127.0.0.1:8000/hook", "events": ["create"]}, headers=headers
        )
    ).status_code == 422
    assert (
        await client.post(
            "/api/v1/webhooks", json={"url": "http://192.168.1.10/hook", "events": ["create"]}, headers=headers
        )
    ).status_code == 422
    assert (
        await client.post(
            "/api/v1/webhooks", json={"url": "ftp://example.com/hook", "events": ["create"]}, headers=headers
        )
    ).status_code == 422

    r = await client.post(
        "/api/v1/webhooks", json={"url": "https://hooks.example.com/romdoul", "events": ["create"]}, headers=headers
    )
    assert r.status_code == 201


# --------------------------------------------------------------------------- #
# Open API: reads/exports/stats are keyless; role checks apply only when a
# session or key IS presented; admin surface stays gated.
# --------------------------------------------------------------------------- #
async def test_records_reads_are_open_without_credentials(client):
    assert (await client.get("/api/v1/records")).status_code == 200
    assert (await client.get("/api/v1/stats")).status_code == 200
    assert (await client.get("/api/v1/meta")).status_code == 200
    assert (await client.get("/api/v1/export", params={"format": "json"})).status_code == 200


async def test_record_writes_are_open_without_credentials(client):
    r = await client.post("/api/v1/records", json={"id": "open-1", "type": "invoice", "data": {"n": 1}})
    assert r.status_code == 201
    r = await client.patch("/api/v1/records/open-1", json={"data": {"n": 2}})
    assert r.status_code == 200
    assert r.json()["edited_by"] == "system:api"
    assert (await client.delete("/api/v1/records/open-1")).status_code == 204


async def test_viewer_session_still_blocked_from_writes(client, monkeypatch):
    from app import config
    from app.security import seed_admin

    monkeypatch.setattr(config.settings, "admin_username", "admin")
    monkeypatch.setattr(config.settings, "admin_password", "admin-pass-123")
    await seed_admin()
    admin_token = (
        await client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin-pass-123"})
    ).json()["token"]
    await client.post(
        "/api/v1/auth/users",
        json={"username": "dara", "password": "dara-pass-123", "role": "viewer"},
        headers={"X-Session-Token": admin_token},
    )
    viewer_token = (
        await client.post("/api/v1/auth/login", json={"username": "dara", "password": "dara-pass-123"})
    ).json()["token"]

    await client.post("/api/v1/records", json={"id": "viewer-block", "type": "invoice", "data": {"n": 1}})
    r = await client.patch(
        "/api/v1/records/viewer-block", json={"data": {"n": 2}}, headers={"X-Session-Token": viewer_token}
    )
    assert r.status_code == 403
    r = await client.delete("/api/v1/records/viewer-block", headers={"X-Session-Token": viewer_token})
    assert r.status_code == 403


async def test_admin_surface_stays_gated(client):
    assert (await client.get("/api/v1/settings")).status_code == 401
    assert (await client.get("/api/v1/audit")).status_code == 401
    assert (await client.get("/api/v1/webhooks")).status_code == 401
    assert (await client.get("/api/v1/auth/me")).status_code == 401
