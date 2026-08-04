async def _seed_admin(monkeypatch):
    from app import config

    monkeypatch.setattr(config.settings, "admin_username", "admin")
    monkeypatch.setattr(config.settings, "admin_password", "admin-pass-123")
    from app.security import seed_admin

    await seed_admin()


async def _login(client, username="admin", password="admin-pass-123"):
    r = await client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200
    return r.json()


async def test_login_wrong_credentials(client, monkeypatch):
    await _seed_admin(monkeypatch)
    r = await client.post("/api/v1/auth/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401

    r = await client.post("/api/v1/auth/login", json={"username": "nobody", "password": "admin-pass-123"})
    assert r.status_code == 401


async def test_login_me_and_reads(client, monkeypatch):
    await _seed_admin(monkeypatch)
    body = await _login(client)
    token = body["token"]
    assert body["user"] == {"username": "admin", "role": "admin"}

    r = await client.get("/api/v1/auth/me", headers={"X-Session-Token": token})
    assert r.status_code == 200
    assert r.json() == {"username": "admin", "role": "admin"}

    # reads without credentials are blocked
    assert (await client.get("/api/v1/records")).status_code == 401
    assert (await client.get("/api/v1/stats")).status_code == 401

    # reads with the session token work
    assert (await client.get("/api/v1/records", headers={"X-Session-Token": token})).status_code == 200
    assert (await client.get("/api/v1/stats", headers={"X-Session-Token": token})).status_code == 200


async def test_logout_revokes_session(client, monkeypatch):
    await _seed_admin(monkeypatch)
    body = await _login(client)
    token = body["token"]

    r = await client.post("/api/v1/auth/logout", headers={"X-Session-Token": token})
    assert r.status_code == 200

    r = await client.get("/api/v1/records", headers={"X-Session-Token": token})
    assert r.status_code == 401


async def test_patch_attribution_uses_username(client, monkeypatch):
    await _seed_admin(monkeypatch)
    token = (await _login(client))["token"]
    headers = {"X-Session-Token": token}

    await client.post("/api/v1/records", json={"type": "invoice", "data": {"n": 1}})
    r = await client.patch("/api/v1/records", json={}, headers=headers)
    # no id → 404; use a real one
    r = await client.get("/api/v1/records", headers=headers)
    record_id = r.json()["items"][0]["id"]
    r = await client.patch(f"/api/v1/records/{record_id}", json={"data": {"n": 2}}, headers=headers)
    assert r.status_code == 200
    assert r.json()["edited_by"] == "user:admin"


async def test_api_key_still_works(client, monkeypatch):
    from app import config

    monkeypatch.setattr(config.settings, "api_keys", "machine-key-1")
    r = await client.get("/api/v1/records", headers={"X-API-Key": "machine-key-1"})
    assert r.status_code == 200
    r = await client.get("/api/v1/records", headers={"X-API-Key": "nope"})
    assert r.status_code == 401


async def test_post_records_stays_open(client, monkeypatch):
    r = await client.post("/api/v1/records", json={"type": "invoice", "data": {"n": 1}})
    assert r.status_code == 201


async def test_admin_can_create_users(client, monkeypatch):
    await _seed_admin(monkeypatch)
    token = (await _login(client))["token"]
    headers = {"X-Session-Token": token}

    r = await client.post("/api/v1/auth/users", json={"username": "dara", "password": "dara-pass-123", "role": "viewer"}, headers=headers)
    assert r.status_code == 201
    assert r.json() == {"username": "dara", "role": "viewer"}

    r = await client.post("/api/v1/auth/users", json={"username": "dara", "password": "dara-pass-123"}, headers=headers)
    assert r.status_code == 409

    # the new user can log in and read
    body = await _login(client, "dara", "dara-pass-123")
    assert body["user"] == {"username": "dara", "role": "viewer"}
    assert (await client.get("/api/v1/records", headers={"X-Session-Token": body["token"]})).status_code == 200


async def test_non_admin_cannot_create_users(client, monkeypatch):
    await _seed_admin(monkeypatch)
    admin_token = (await _login(client))["token"]
    await client.post("/api/v1/auth/users", json={"username": "dara", "password": "dara-pass-123", "role": "viewer"}, headers={"X-Session-Token": admin_token})

    viewer_token = (await _login(client, "dara", "dara-pass-123"))["token"]
    r = await client.post("/api/v1/auth/users", json={"username": "bob", "password": "bob-pass-123"}, headers={"X-Session-Token": viewer_token})
    assert r.status_code == 403
