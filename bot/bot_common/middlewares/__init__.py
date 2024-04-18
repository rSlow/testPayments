from aiogram import BaseMiddleware, Router


def register_middlewares(router: Router,
                         middlewares: list[BaseMiddleware]):
    for middleware in middlewares:
        router.message.middleware(middleware)
        router.callback_query.middleware(middleware)
        router.error.middleware(middleware)
