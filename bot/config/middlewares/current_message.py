from abc import abstractmethod
from typing import Callable, Dict, Any, Awaitable, Optional, Protocol

from aiogram import BaseMiddleware, types, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, InlineKeyboardMarkup


class EditCallback(Protocol):
    @abstractmethod
    async def __call__(self,
                       text: str,
                       reply_markup: Optional[InlineKeyboardMarkup] = None) -> types.Message:
        ...


class DeleteMarkupCallback(Protocol):
    @abstractmethod
    async def __call__(self) -> types.Message:
        ...


def edit_callback(bot: Bot,
                  chat_id: str | int,
                  message_id: str | int) -> EditCallback:
    async def edit_message(text: str,
                           reply_markup: Optional[InlineKeyboardMarkup] = None):
        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup
        )

    return edit_message


def delete_markup_callback(bot: Bot,
                           chat_id: str | int,
                           message_id: str | int) -> Callable:
    async def delete_markup():
        try:
            return await bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=message_id,
            )
        except TelegramBadRequest:
            pass

    return delete_markup


class ActiveMessageMiddleware(BaseMiddleware):
    active_message_id = "active_message_id"
    chat_id = "chat_id"

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        state: FSMContext = data["state"]
        bot: Bot = data["bot"]

        state_data = await state.get_data()
        active_message_id = state_data.get(self.active_message_id)
        chat_id = state_data.get(self.chat_id)

        data.update({
            self.active_message_id: active_message_id,
            self.chat_id: chat_id,
            "edit_callback": edit_callback(
                bot=bot,
                chat_id=chat_id,
                message_id=active_message_id
            ),
            "delete_markup_callback": delete_markup_callback(
                bot=bot,
                chat_id=chat_id,
                message_id=active_message_id
            )
        })

        result = await handler(event, data)

        if isinstance(result, types.Message):
            await state.update_data(
                {
                    self.active_message_id: result.message_id,
                    self.chat_id: state.key.chat_id,
                }
            )
        return result
