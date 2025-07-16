import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from app.config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "bot.log"

_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when="D", interval=1, backupCount=7, encoding="utf-8"
    )
    file_handler.setFormatter(_formatter)

    console = logging.StreamHandler()
    console.setFormatter(_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console)
    logger.propagate = False
    return logger

logger = get_logger()