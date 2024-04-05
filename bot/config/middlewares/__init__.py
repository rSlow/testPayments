from aiogram import BaseMiddleware, Router


def register_middlewares(router: Router,
                         middlewares: list[BaseMiddleware]):
    for middleware in middlewares:
        router.message.middleware.register(middleware)
        router.callback_query.middleware.register(middleware)
        router.error.middleware.register(middleware)
