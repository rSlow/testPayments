from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from aiohttp import ClientSession

from config.logging import init_logging
from config.middlewares import register_middlewares
from config.ui_commands import set_ui_commands
from config.middlewares.client_session import ContextMiddleware

from apps.products.api import BackendAPI


async def on_startup(dispatcher: Dispatcher,
                     bot: Bot):
    setup_dialogs(dispatcher)
    init_logging()
    await set_ui_commands(bot)
    register_middlewares(
        dispatcher=dispatcher,
        middlewares=[
            ContextMiddleware(
                session=ClientSession()
            ),
            CallbackAnswerMiddleware()
        ]
    )
