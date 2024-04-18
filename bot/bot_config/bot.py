from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation

from bot_apps.router import apps_router
from bot_common.handlers.error import error_router
from bot_common.handlers.start import start_router, start_dialog
from .settings import ENV
from .storage import redis_storage

API_TOKEN = ENV.str("TELEGRAM_API_TOKEN")
bot = Bot(
    token=API_TOKEN,
    parse_mode="HTML"
)

dispatcher = Dispatcher(
    storage=redis_storage,
    events_isolation=SimpleEventIsolation()
)

dispatcher.include_routers(
    error_router,
    start_router,
    apps_router,
    start_dialog,
)
