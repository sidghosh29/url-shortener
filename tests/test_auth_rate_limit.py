import pytest


@pytest.fixture
def signin_client(client):
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app, client=("192.0.2.10", 50000)) as test_client:
        yield test_client


def test_signin_is_limited_to_five_attempts_per_minute(client, signin_client):
    credentials = {
        "username": "rate-limit-user",
        "email": "rate-limit-user@example.com",
        "password": "correct-test-password",
    }
    registration = client.post("/api/register", json=credentials)
    assert registration.status_code == 201

    for _ in range(5):
        response = signin_client.post(
            "/api/signin",
            json={
                "username": credentials["username"],
                "password": "wrong-password",
            },
        )
        assert response.status_code == 401

    limited_response = signin_client.post(
        "/api/signin",
        json={
            "username": credentials["username"],
            "password": "wrong-password",
        },
    )
    assert limited_response.status_code == 429
