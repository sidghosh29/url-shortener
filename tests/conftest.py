import os
from pathlib import Path

import pytest

os.environ.update(
    {
        "DATABASE_URL": (
            "postgresql+psycopg://postgres:postgres@localhost:5432/url_shortener_test"
        ),
        "REDIS_URL": "redis://localhost:6379/1",
        "SLOWAPI_STORAGE_URI": "memory://",
        "BASE_URL": "http://localhost:8000",
        "LUA_FOLDER_PATH": "app/lua",
        "RATE_LIMIT_CAPACITY": "100000",
        "RATE_LIMIT_WINDOW": "60",
        "JWT_SECRET_KEY": "test-only-secret-key-not-for-production",
        "JWT_ALGORITHM": "HS256",
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES": "15",
    }
)


@pytest.fixture(scope="session", autouse=True)
def migrate_test_database():
    """Bring the dedicated test database to the same schema as production."""
    from alembic import command
    from alembic.config import Config

    project_root = Path(__file__).resolve().parents[1]
    command.upgrade(Config(str(project_root / "alembic.ini")), "head")


@pytest.fixture
def client():
    # Import after test-specific settings and migrations are ready.
    from fastapi.testclient import TestClient

    from app.database import SessionLocal
    from app.main import app
    from app.models import Url, User

    def clear_test_rows():
        with SessionLocal() as db:
            db.query(Url).delete()
            db.query(User).delete()
            db.commit()

    with TestClient(app) as test_client:
        clear_test_rows()
        yield test_client
        clear_test_rows()


@pytest.fixture
def auth_headers(client):
    credentials = {
        "username": "pytest-user",
        "email": "pytest-user@example.com",
        "password": "pytest-password",
    }
    registration = client.post("/api/register", json=credentials)
    assert registration.status_code == 201, registration.text

    signin = client.post(
        "/api/signin",
        json={
            "username": credentials["username"],
            "password": credentials["password"],
        },
    )
    assert signin.status_code == 200, signin.text
    return {"Authorization": f"Bearer {signin.json()['access_token']}"}
