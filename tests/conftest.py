import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:postgres@localhost:5432/url_shortener_test"
)
os.environ["REDIS_URL"] = "redis://localhost:6379/1"


import pytest


@pytest.fixture
def client():
    # Import after DATABASE_URL and REDIS_URL have been set.
    from fastapi.testclient import TestClient

    from app.database import SessionLocal
    from app.main import app
    from app.models import Url

    def clear_urls():
        with SessionLocal() as db:
            db.query(Url).delete()
            db.commit()

    with TestClient(app) as test_client:
        clear_urls()
        yield test_client
        clear_urls()
