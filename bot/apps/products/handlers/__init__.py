from aiogram import Router

from .category import category_router
from .subcategory import subcategory_router

products_router = Router(name="products")

products_router.include_routers(
    category_router,
    subcategory_router,
)
