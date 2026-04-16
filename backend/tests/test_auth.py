from conftest import make_user_payload, VALID_PASSWORD


def test_login_valid(client):
    payload = make_user_payload()
    client.post("/users", json=payload)

    res = client.post("/auth/login", json={"email": payload["email"], "password": VALID_PASSWORD})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    payload = make_user_payload()
    client.post("/users", json=payload)

    res = client.post("/auth/login", json={"email": payload["email"], "password": "WrongPass1!"})
    assert res.status_code == 401


def test_login_nonexistent_email(client):
    res = client.post("/auth/login", json={"email": "nobody@test.com", "password": VALID_PASSWORD})
    assert res.status_code == 401


def test_refresh_valid_cookie(client):
    payload = make_user_payload()
    client.post("/users", json=payload)

    # TestClient mantém cookies automaticamente entre chamadas
    login_res = client.post("/auth/login", json={"email": payload["email"], "password": VALID_PASSWORD})
    assert login_res.status_code == 200

    res = client.post("/auth/refresh")
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_refresh_no_cookie(client):
    res = client.post("/auth/refresh")
    assert res.status_code == 401


def test_logout(client):
    res = client.post("/auth/logout")
    assert res.status_code == 200
    assert res.json()["message"] == "Logout realizado"
