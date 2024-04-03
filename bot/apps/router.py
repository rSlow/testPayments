from aiogram import Router

from .products.handlers import products_router

apps_router = Router(name="apps")

apps_router.include_routers(
    products_router,
)
