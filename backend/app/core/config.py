from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "enterprise-ai-agent"
    app_env: str = "development"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./enterprise_ai.db")
    secret_key: str = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-me")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def get_settings() -> Settings:
    return Settings()
