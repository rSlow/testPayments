from aiogram import Dispatcher, BaseMiddleware


def register_middlewares(dispatcher: Dispatcher,
                         middlewares: list[BaseMiddleware]):
    for middleware in middlewares:
        dispatcher.update.middleware.register(middleware)
        dispatcher.error.middleware.register(middleware)
