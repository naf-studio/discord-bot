"""Runtime configuration management using Pydantic Settings."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application settings resolved from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: str = Field(..., description="Discord Bot Authentication Token")
    permissions: int = Field(default=8, description="OAuth2 permission integer")
    discord_invite_link: str = Field(
        default="http://dsc.gg/nafd",
        description="Public Discord invite URL",
    )
    join_channel_id: int = Field(
        default=0, description="Audit channel ID for member join events"
    )
    leave_channel_id: int = Field(
        default=0, description="Audit channel ID for member leave events"
    )
    boost_channel_id: int = Field(
        default=0, description="Channel ID for nitro boost announcements"
    )
    owner_id: int = Field(
        default=0, description="Discord user ID of the primary bot operator"
    )
    sync_commands_on_startup: bool = Field(
        default=False,
        description="Whether to synchronize application commands on startup",
    )
    messages_dir: Path = Field(
        default=PROJECT_ROOT / "config" / "messages",
        description="Absolute path to message templates directory",
    )
    log_level: str = Field(default="INFO", description="Console and file logging level")


def get_settings() -> Settings:
    """Instantiate and return application settings singleton."""
    return Settings()
