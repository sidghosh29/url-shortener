from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers.urls import router as urls_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


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
