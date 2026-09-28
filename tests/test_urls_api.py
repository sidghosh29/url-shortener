from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_short_url():
    response = client.post(
        "/shorten",
        json={"url": "https://www.google.com"},
    )

    assert response.status_code == 201

    data = response.json()

    assert "short_code" in data
    assert data["short_url"] == f"http://localhost:8000/{data['short_code']}"
