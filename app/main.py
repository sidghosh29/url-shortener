import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.logging_config import configure_logging  # noqa

configure_logging()  # noqa

from app.database import engine  # noqa
from app.dependencies.auth import ensure_bearer  # noqa
from app.middleware.auth import JWTAuthMiddleware  # noqa
from app.models import Base  # noqa
from app.routers.urls import router as urls_router  # noqa
from app.routers.auth import router as user_router  # noqa

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")


app = FastAPI(
    lifespan=lifespan,
    title="URL Shortener API",
    version="1.0.0",
    description="A simple URL shortening service built with FastAPI",
    dependencies=[Depends(ensure_bearer)],
)
# The lifespan function is an asynchronous context manager
# that runs setup code before the application starts and
# cleanup code after it shuts down. In this case, it creates
# the database tables before the app starts.

app.add_middleware(JWTAuthMiddleware)


@app.get("/")
def root():
    return {"message": "URL Shortener API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(urls_router, prefix="/api")
# This line includes the URL router from the urls module,
# which contains the API endpoints for URL shortening and redirection.

app.include_router(user_router, prefix="/api")
