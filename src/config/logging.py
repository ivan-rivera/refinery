"""Application logging configuration."""

from __future__ import annotations

from logging.config import dictConfig

from src.config.constants import LOG_DATE_FORMAT, LOG_FORMAT


def configure_logging(log_level: str = "INFO") -> None:
    """Configure process-wide logging."""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": LOG_FORMAT,
                    "datefmt": LOG_DATE_FORMAT,
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "handlers": ["default"],
                "level": log_level.upper(),
            },
        },
    )
