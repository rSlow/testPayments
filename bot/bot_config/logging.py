import logging
import os

from bot_config import settings


def init_logging() -> None:
    if not settings.LOGS_DIR.is_dir():
        os.mkdir(settings.LOGS_FOLDER)

    logging.basicConfig(
        level=logging.DEBUG,
        filename=settings.LOGS_DIR / "log.log" if not settings.DEBUG else None,
        format="[%(asctime)s - %(levelname)s] %(name)s - %(message)s",
    )
