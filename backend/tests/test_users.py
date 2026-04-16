from conftest import make_user_payload, VALID_PASSWORD


def test_create_user(client):
    payload = make_user_payload(email="edu@test.com")
    res = client.post("/users", json=payload)
    assert res.status_code == 201
    assert res.json()["email"] == payload["email"]


def test_duplicate_email(client):
    payload = make_user_payload()
    first = client.post("/users", json=payload)
    assert first.status_code == 201

    res = client.post("/users", json=payload)
    assert res.status_code == 400


def test_invalid_email(client):
    payload = make_user_payload(email="nao-e-email")
    res = client.post("/users", json=payload)
    assert res.status_code == 422


def test_password_too_short(client):
    payload = make_user_payload(password="Ab1!")
    res = client.post("/users", json=payload)
    assert res.status_code == 422


def test_password_no_uppercase(client):
    payload = make_user_payload(password="abcdefg1!")
    res = client.post("/users", json=payload)
    assert res.status_code == 422


def test_password_no_number(client):
    payload = make_user_payload(password="Abcdefg!")
    res = client.post("/users", json=payload)
    assert res.status_code == 422


def test_password_no_special(client):
    payload = make_user_payload(password="Abcdefg1")
    res = client.post("/users", json=payload)
    assert res.status_code == 422


def test_get_user_authenticated(auth_user, client):
    user_id = auth_user["id"]
    res = client.get(f"/users/{user_id}", headers=auth_user["headers"])
    assert res.status_code == 200
    assert res.json()["id"] == user_id


def test_get_user_another_user(client):
    payload_a = make_user_payload(email="a@test.com")
    payload_b = make_user_payload(email="b@test.com")

    client.post("/users", json=payload_a)
    user_b_id = client.post("/users", json=payload_b).json()["id"]

    login_res = client.post("/auth/login", json={"email": payload_a["email"], "password": VALID_PASSWORD})
    headers_a = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    res = client.get(f"/users/{user_b_id}", headers=headers_a)
    assert res.status_code == 403


def test_get_user_no_token(client):
    payload = make_user_payload()
    user_id = client.post("/users", json=payload).json()["id"]
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 401


def test_delete_user(auth_user, client):
    user_id = auth_user["id"]
    res = client.delete(f"/users/{user_id}", headers=auth_user["headers"])
    assert res.status_code == 204


def test_delete_another_user(client):
    payload_a = make_user_payload(email="a@test.com")
    payload_b = make_user_payload(email="b@test.com")

    client.post("/users", json=payload_a)
    user_b_id = client.post("/users", json=payload_b).json()["id"]

    login_res = client.post("/auth/login", json={"email": payload_a["email"], "password": VALID_PASSWORD})
    headers_a = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    res = client.delete(f"/users/{user_b_id}", headers=headers_a)
    assert res.status_code == 403
