from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = Env()

DEBUG: bool = ENV.bool("AIOGRAM_DEBUG", False)

REDIS_URL: str = ENV.str("REDIS_URL")

LOGS_FOLDER = ENV.str("LOGS_DIR", "logs")
LOGS_DIR = BASE_DIR / LOGS_FOLDER

GROUP_SUBSCRIBE_ID = ENV.str("GROUP_SUBSCRIBE_ID")
CHANNEL_SUBSCRIBE_ID = ENV.str("CHANNEL_SUBSCRIBE_ID")

LOCAL_BASE = ENV.str("LOCAL_BASE")
GLOBAL_BASE = ENV.str("GLOBAL_BASE", "")
