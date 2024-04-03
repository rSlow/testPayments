from pathlib import Path

from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = get_env()

DEBUG: bool = ENV.bool("AIOGRAM_DEBUG", False)

REDIS_URL: str = ENV.str("REDIS_URL")

LOGS_FOLDER = ENV.str("LOGS_DIR", "logs")
LOGS_DIR = BASE_DIR / LOGS_FOLDER
