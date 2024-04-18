from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from aiohttp import ClientSession

from bot_apps.products.api import ProductsAPI
from bot_common.api import UserAPI
from bot_config import settings
from bot_config.logging import init_logging
from bot_common.middlewares import register_middlewares
from bot_config.ui_commands import set_ui_commands
from bot_common.middlewares.context import ContextMiddleware


async def on_startup(dispatcher: Dispatcher,
                     bot: Bot):
    setup_dialogs(dispatcher)
    init_logging()
    await set_ui_commands(bot)

    register_middlewares(
        router=dispatcher,
        middlewares=[
            ContextMiddleware(
                session=ClientSession(),
                user_api=UserAPI(
                    local_base=settings.LOCAL_BASE
                ),
                product_api=ProductsAPI(
                    local_base=settings.LOCAL_BASE,
                    global_base=settings.GLOBAL_BASE,
                )
            ),
            CallbackAnswerMiddleware()
        ]
    )
