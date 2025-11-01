"""Configuration management for the medication reminder system."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Twilio Configuration
    twilio_account_sid: str = Field(..., env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(..., env="TWILIO_AUTH_TOKEN")
    twilio_phone_number: str = Field(..., env="TWILIO_PHONE_NUMBER")

    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./medication_reminders.db",
        env="DATABASE_URL"
    )

    # Application Settings
    app_name: str = Field(default="Elder Medication Reminder Agent", env="APP_NAME")
    timezone: str = Field(default="America/New_York", env="TIMEZONE")

    # Caregiver Settings
    caregiver_notification_delay_minutes: int = Field(
        default=15,
        env="CAREGIVER_NOTIFICATION_DELAY_MINUTES"
    )
    max_reminder_attempts: int = Field(default=3, env="MAX_REMINDER_ATTEMPTS")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global settings
    if settings is None:
        settings = Settings()
    return settings
