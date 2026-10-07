from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    BASE_URL: str
    REDIS_URL: str
    LUA_FOLDER_PATH: str
    RATE_LIMIT_CAPACITY: int
    RATE_LIMIT_WINDOW: int
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# from dotenv import load_dotenv
# from os import getenv

# load_dotenv()

# DATABASE_URL = getenv("DATABASE_URL")
# BASE_URL = getenv("BASE_URL")
# RATE_LIMIT_CAPACITY = int(getenv("RATE_LIMIT_CAPACITY"))
# RATE_LIMIT_WINDOW = int(getenv("RATE_LIMIT_WINDOW"))
