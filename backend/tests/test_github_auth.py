from unittest.mock import patch
from fastapi import HTTPException
from conftest import make_user_payload

FAKE_GITHUB_INFO = {"github_id": "github_123", "email": "githubuser@test.com", "name": "GitHub User"}


def _mock_verify(info=FAKE_GITHUB_INFO):
    return patch("routers.auth.verify_github_token", return_value=info)


def test_github_auth_creates_new_user(client):
    with _mock_verify():
        res = client.post("/auth/github", json={"code": "fake_code"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_github_auth_sets_refresh_cookie(client):
    with _mock_verify():
        res = client.post("/auth/github", json={"code": "fake_code"})
    assert "refresh_token" in res.cookies


def test_github_auth_existing_user_by_github_id(client):
    with _mock_verify():
        client.post("/auth/github", json={"code": "fake_code"})
        res = client.post("/auth/github", json={"code": "fake_code"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_github_auth_links_existing_email_user(client):
    payload = make_user_payload(email=FAKE_GITHUB_INFO["email"])
    client.post("/users", json=payload)

    with _mock_verify():
        res = client.post("/auth/github", json={"code": "fake_code"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_github_auth_invalid_code(client):
    with patch("routers.auth.verify_github_token", side_effect=HTTPException(status_code=401, detail="Código GitHub inválido ou expirado")):
        res = client.post("/auth/github", json={"code": "bad_code"})
    assert res.status_code == 401
