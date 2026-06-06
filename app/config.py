from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    BASE_URL: str
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )
settings = Settings()

# from dotenv import load_dotenv
# from os import getenv

# load_dotenv()

# DATABASE_URL = getenv("DATABASE_URL")
# BASE_URL = getenv("BASE_URL")