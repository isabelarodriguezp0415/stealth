"""Main entry point for the Elder Medication Reminder Agent."""

import sys
import signal
from pathlib import Path
from loguru import logger

from .config import get_settings
from .service import MedicationReminderService


def setup_logging():
    """Configure logging for the application."""
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )

    # Add file handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "medication_reminder_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="30 days",
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
    )


def main():
    """Main entry point."""
    # Setup logging
    setup_logging()

    logger.info("=" * 70)
    logger.info("Elder Medication Reminder Agent")
    logger.info("=" * 70)

    # Check for .env file
    env_file = Path(".env")
    if not env_file.exists():
        logger.warning(
            ".env file not found. Please copy .env.example to .env "
            "and configure your settings."
        )
        logger.info("Creating .env from .env.example...")
        try:
            from shutil import copy
            copy(".env.example", ".env")
            logger.info(".env file created. Please configure it with your API keys.")
            return 1
        except Exception as e:
            logger.error(f"Failed to create .env file: {e}")
            return 1

    # Initialize service
    service = MedicationReminderService()

    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        service.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Initialize the service
        service.initialize()

        logger.info("Service is running. Press Ctrl+C to stop.")
        logger.info(
            "You can now use the AI agent to manage medications via "
            "natural language or integrate with your application."
        )

        # Keep the main thread alive
        signal.pause()

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Error running service: {e}", exc_info=True)
        return 1
    finally:
        service.shutdown()

    return 0


if __name__ == "__main__":
    sys.exit(main())
