from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs

from bot.config.logging import init_logging
from bot.config.middlewares.current_message import ActiveMessageMiddleware
from bot.config.middlewares import register_middlewares
from bot.config.ui_commands import set_ui_commands


async def on_startup(dispatcher: Dispatcher,
                     bot: Bot):
    setup_dialogs(dispatcher)
    init_logging()
    await set_ui_commands(bot)
    register_middlewares(
        dispatcher=dispatcher,
        middlewares=[
            ActiveMessageMiddleware(),
            CallbackAnswerMiddleware()
        ]
    )
