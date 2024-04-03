import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramMigrateToChat


async def is_subscribed_to(bot: Bot,
                           chat_id: int | str,
                           user_id: int | str):
    try:
        user_status = await bot.get_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )
        if user_status.status.value == "left":
            return False
        return True
    except (TelegramBadRequest, TelegramMigrateToChat) as ex:
        print(chat_id)
        logging.exception(ex)
