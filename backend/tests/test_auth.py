async def test_api_key_required_when_configured(client, monkeypatch):
    from app import config

    original = config.settings.api_keys
    config.settings.api_keys = "secret-key-1"
    try:
        r = await client.get("/api/v1/records")
        assert r.status_code == 401

        r = await client.get("/api/v1/records", headers={"X-API-Key": "secret-key-1"})
        assert r.status_code == 200

        r = await client.get("/api/v1/records", headers={"X-API-Key": "wrong"})
        assert r.status_code == 401
    finally:
        config.settings.api_keys = original


async def test_login_flow(client, monkeypatch):
    from app import config

    original = config.settings.api_keys
    config.settings.api_keys = "secret-key-1"
    try:
        r = await client.post("/api/v1/auth/login", json={"password": "wrong"})
        assert r.status_code == 401

        r = await client.post("/api/v1/auth/login", json={"password": "secret-key-1"})
        assert r.status_code == 200
        token = r.json()["token"]
        assert token == "secret-key-1"

        r = await client.get("/api/v1/stats", headers={"X-API-Key": token})
        assert r.status_code == 200
    finally:
        config.settings.api_keys = original


async def test_login_disabled_without_keys(client, monkeypatch):
    from app import config

    original = config.settings.api_keys
    config.settings.api_keys = ""
    try:
        r = await client.post("/api/v1/auth/login", json={"password": "anything"})
        assert r.status_code == 403
    finally:
        config.settings.api_keys = original


async def test_post_records_stays_open_when_keys_configured(client, monkeypatch):
    from app import config

    original = config.settings.api_keys
    config.settings.api_keys = "secret-key-1"
    try:
        r = await client.post("/api/v1/records", json={
            "type": "invoice", "data": {"n": 1},
        })
        assert r.status_code == 201

        r = await client.get("/api/v1/records")
        assert r.status_code == 401
    finally:
        config.settings.api_keys = original
