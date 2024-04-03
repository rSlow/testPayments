from pathlib import Path

from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent
ENV = get_env(BASE_DIR)
