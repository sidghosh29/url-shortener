import logging
import os
from logging.handlers import RotatingFileHandler

VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def get_log_level(level_name: str) -> int:
    level_name = level_name.upper()
    if level_name not in VALID_LOG_LEVELS:
        raise ValueError(
            f"Invalid LOG_LEVEL={level_name!r}. Choose from: "
            f"{', '.join(sorted(VALID_LOG_LEVELS))}"
        )
    return getattr(logging, level_name)


def configure_logging() -> None:
    level = get_log_level(os.getenv("LOG_LEVEL", "INFO"))
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    handlers: list[logging.Handler] = [logging.StreamHandler()]
    log_file = os.getenv("LOG_FILE")
    if log_file:
        handlers.append(
            RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            )
        )

    for handler in handlers:
        handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=handlers, force=True)

    # Route Uvicorn records through the same handlers and formatter.
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.setLevel(level)
        uvicorn_logger.propagate = True
