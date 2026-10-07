"""Application entrypoint and logger configuration for the NAF Studio Discord Bot."""

import logging
import sys
from logging.handlers import RotatingFileHandler

from pydantic import ValidationError

from discord_bot.bot import CommunityBot
from discord_bot.config import PROJECT_ROOT, get_settings


def configure_logging(log_level_name: str = "INFO") -> None:
    """Set up console and rotating file logging handlers."""
    log_level = getattr(logging, log_level_name.upper(), logging.INFO)
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    file_handler = RotatingFileHandler(
        filename=logs_dir / "bot.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def main() -> None:
    """Validate runtime configuration and start the Discord bot process."""
    try:
        settings = get_settings()
    except ValidationError as exc:
        print(f"CRITICAL: Invalid or incomplete configuration: {exc}", file=sys.stderr)
        sys.exit(1)

    configure_logging(settings.log_level)
    logger = logging.getLogger(__name__)

    if not settings.bot_token or settings.bot_token == "your_bot_token_here":
        logger.critical(
            "BOT_TOKEN is missing or using default placeholder. Please configure .env."
        )
        sys.exit(1)

    bot = CommunityBot(settings=settings)
    try:
        bot.run(settings.bot_token, reconnect=True)
    except KeyboardInterrupt:
        logger.info("Process interrupted by user. Exiting gracefully.")
    except Exception as exc:
        logger.critical("Fatal error encountered during bot execution: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
