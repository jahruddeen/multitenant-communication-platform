
from dotenv import load_dotenv

load_dotenv()

import os
from functools import lru_cache


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "Automated SMS Voice Platform"
    )

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "CHANGE_THIS_SECRET_IN_PRODUCTION"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./notifications.db"
    )

    PROVIDER_MODE = os.getenv(
        "PROVIDER_MODE",
        "mock"
    ).lower()

    MAX_CALL_ATTEMPTS = int(
        os.getenv("MAX_CALL_ATTEMPTS", "3")
    )

    CALL_RETRY_COOLDOWN_MINUTES = int(
        os.getenv("CALL_RETRY_COOLDOWN_MINUTES", "60")
    )

    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173"
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()