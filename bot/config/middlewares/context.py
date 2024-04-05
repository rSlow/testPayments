from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ContextMiddleware(BaseMiddleware):
    def __init__(self, **context):
        super().__init__()
        self.context = context

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        data.update(self.context)
        await handler(event, data)
