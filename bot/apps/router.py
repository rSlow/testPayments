from aiogram import Router

from .products.handlers import products_dialog

apps_router = Router(name="apps")

apps_router.include_routers(
    products_dialog,
)
