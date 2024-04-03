import logging

from aiogram import Bot, Dispatcher

from config.logging import init_logging
from config.milldewares import register_middlewares
from config.ui_commands import set_ui_commands


async def on_startup(dispatcher: Dispatcher,
                     bot: Bot):
    init_logging()
    await set_ui_commands(bot)
    register_middlewares(
        dispatcher=dispatcher,
        middlewares=[]
    )
    logging.info("123")
