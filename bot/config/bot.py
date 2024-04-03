from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation

from apps.router import apps_router
from common.handlers.delete import delete_router
from common.handlers.error import error_router
from common.handlers.start import start_router
from .settings import ENV
from .storage import redis_storage

API_TOKEN = ENV.str("TELEGRAM_API_TOKEN")
bot = Bot(token=API_TOKEN)

dispatcher = Dispatcher(
    storage=redis_storage,
    events_isolation=SimpleEventIsolation()
)

dispatcher.include_routers(
    start_router,
    error_router,
    apps_router,
    delete_router
)
