"""Centralised application settings loaded from environment variables.

Uses ``pydantic-settings`` (Pydantic v2) so every value is typed, validated
and available through a single cached ``Settings`` instance.
"""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings.

    All values are read from the process environment (or a local ``.env``
    file in development). Anything sensitive must be supplied via environment
    variables in production (Render dashboard, Docker secrets, etc.).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ---- Application ----
    APP_NAME: str = "Unique Nurse and Aya Services"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ---- Security / JWT ----
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30

    # ---- Database ----
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "unique_nurse_aya"

    # ---- Cloudinary ----
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    CLOUDINARY_URL: str = ""

    # ---- Email (Resend) ----
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "Unique Nurse and Aya Services <onboarding@resend.dev>"
    EMAIL_FROM_NAME: str = "Unique Nurse and Aya Services"
    ADMIN_NOTIFICATION_EMAIL: str = ""


    # ---- CORS ----
    # Comma-separated string in the environment; use ``cors_origins`` for the
    # parsed list (avoids pydantic-settings JSON-decoding complex env values).
    CORS_ORIGINS: str = "*"

    # ---- Rate limiting ----
    RATE_LIMIT_DEFAULT: str = "200/minute"
    RATE_LIMIT_AUTH: str = "10/minute"

    # ---- Frontend ----
    FRONTEND_URL: str = "http://localhost:3000"

    # ---- Bootstrap admin ----
    FIRST_ADMIN_NAME: str = "Super Admin"
    FIRST_ADMIN_EMAIL: str = "admin@uniquenurseaya.com"
    FIRST_ADMIN_PASSWORD: str = "Admin@1234Secure!"

    @property
    def cors_origins(self) -> List[str]:
        """Return CORS origins parsed from the comma-separated string.

        Production front-ends are always allowed so the deployed admin and
        website keep working even if the ``CORS_ORIGINS`` env var is missing
        or out of date. Credentialed requests can't use a ``*`` wildcard, so
        an explicit list is always returned.
        """
        # Baked-in allowlist: live domains + local dev origins.
        origins: List[str] = [
            "https://admin.uniquenursing.in",
            "https://uniquenursing.in",
            "https://www.uniquenursing.in",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8080",
        ]
        raw = self.CORS_ORIGINS.strip()
        if raw and raw != "*":
            origins.extend(
                origin.strip() for origin in raw.split(",") if origin.strip()
            )
        # De-duplicate while preserving order.
        seen: set[str] = set()
        return [o for o in origins if not (o in seen or seen.add(o))]

    @property
    def is_production(self) -> bool:
        """Return ``True`` when running in a production-like environment."""
        return self.APP_ENV.lower() in {"production", "prod"}

    @property
    def email_enabled(self) -> bool:
        """Return ``True`` only when Resend API key is configured."""
        return bool(self.RESEND_API_KEY)

    @property
    def cloudinary_enabled(self) -> bool:
        """Return ``True`` only when Cloudinary credentials are present."""
        return bool(
            self.CLOUDINARY_CLOUD_NAME
            and self.CLOUDINARY_API_KEY
            and self.CLOUDINARY_API_SECRET
        )


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance (dependency-injectable)."""
    return Settings()  # type: ignore[call-arg]


# Module-level singleton for convenient imports.
settings: Settings = get_settings()
