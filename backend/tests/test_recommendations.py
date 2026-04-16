import models
from conftest import make_user_payload, VALID_PASSWORD


def _insert_matching_job(db):
    """Insere uma vaga que dá match alto com skills ['python', 'fastapi']."""
    job = models.Job(
        title="Python FastAPI Developer",
        description="Vaga para desenvolvedor Python com experiência em FastAPI",
        url="http://jobs.test/python-fastapi-dev",
        source="test",
        company="Test Co",
        location="Remote",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def _login(client, email, password=VALID_PASSWORD):
    res = client.post("/auth/login", json={"email": email, "password": password})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def test_list_recommendations_empty(auth_user, client):
    user_id = auth_user["id"]
    res = client.get(f"/users/{user_id}/recommendations", headers=auth_user["headers"])
    assert res.status_code == 200
    assert res.json() == []


def test_list_recommendations_with_data(client, db):
    # Vaga inserida antes da criação do usuário para o matcher processá-la
    _insert_matching_job(db)

    payload = make_user_payload()
    user_id = client.post("/users", json=payload).json()["id"]
    headers = _login(client, payload["email"])

    res = client.get(f"/users/{user_id}/recommendations", headers=headers)
    assert res.status_code == 200
    recs = res.json()
    assert len(recs) >= 1
    scores = [r["match_score"] for r in recs]
    assert scores == sorted(scores, reverse=True)


def test_list_recommendations_another_user(client):
    payload_a = make_user_payload(email="a@test.com")
    payload_b = make_user_payload(email="b@test.com")

    client.post("/users", json=payload_a)
    user_b_id = client.post("/users", json=payload_b).json()["id"]

    headers_a = _login(client, payload_a["email"])

    res = client.get(f"/users/{user_b_id}/recommendations", headers=headers_a)
    assert res.status_code == 403


def test_update_recommendation_applied(client, db):
    _insert_matching_job(db)

    payload = make_user_payload()
    user_id = client.post("/users", json=payload).json()["id"]
    headers = _login(client, payload["email"])

    rec_id = client.get(f"/users/{user_id}/recommendations", headers=headers).json()[0]["id"]

    res = client.patch(f"/users/{user_id}/recommendations/{rec_id}", json={"status": "applied"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["status"] == "applied"


def test_update_recommendation_rejected(client, db):
    _insert_matching_job(db)

    payload = make_user_payload()
    user_id = client.post("/users", json=payload).json()["id"]
    headers = _login(client, payload["email"])

    rec_id = client.get(f"/users/{user_id}/recommendations", headers=headers).json()[0]["id"]

    res = client.patch(f"/users/{user_id}/recommendations/{rec_id}", json={"status": "rejected"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["status"] == "rejected"


def test_update_recommendation_invalid_status(auth_user, client):
    user_id = auth_user["id"]
    res = client.patch(
        f"/users/{user_id}/recommendations/999",
        json={"status": "foo"},
        headers=auth_user["headers"],
    )
    assert res.status_code == 422


def test_update_recommendation_wrong_user(client, db):
    """Usuário A tenta atualizar a recomendação do usuário B via sua própria URL → 404."""
    _insert_matching_job(db)

    payload_a = make_user_payload(email="a@test.com")
    payload_b = make_user_payload(email="b@test.com")

    user_a_id = client.post("/users", json=payload_a).json()["id"]
    user_b_id = client.post("/users", json=payload_b).json()["id"]

    headers_a = _login(client, payload_a["email"])
    headers_b = _login(client, payload_b["email"])

    # Pega o id da recomendação do usuário B
    rec_b_id = client.get(f"/users/{user_b_id}/recommendations", headers=headers_b).json()[0]["id"]

    # Usuário A tenta atualizar a rec do B usando o próprio user_id na URL
    res = client.patch(
        f"/users/{user_a_id}/recommendations/{rec_b_id}",
        json={"status": "applied"},
        headers=headers_a,
    )
    assert res.status_code == 404
