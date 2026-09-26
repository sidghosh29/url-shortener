import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.logging_config import configure_logging  # noqa

configure_logging()  # noqa

from app.database import engine  # noqa
from app.models import Base  # noqa
from app.routers.urls import router as urls_router  # noqa

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        logger.exception("Application startup failed while initializing database")
        raise
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan)
# The lifespan function is an asynchronous context manager
# that runs setup code before the application starts and
# cleanup code after it shuts down. In this case, it creates
# the database tables before the app starts.


@app.get("/")
def root():
    return {"message": "URL Shortener API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(urls_router)
# This line includes the URL router from the urls module,
# which contains the API endpoints for URL shortening and redirection.
