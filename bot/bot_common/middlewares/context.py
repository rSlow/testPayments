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
        return await handler(event, data)

    def __str__(self):
        return f"{self.__class__.__name__} {[str(context) for context in self.context.values()]}"

    __repr__ = __str__
