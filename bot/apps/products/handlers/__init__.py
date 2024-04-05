from aiogram_dialog import Dialog

from config.middlewares import register_middlewares
from config.middlewares.context import ContextMiddleware
from .add_product import set_count_window, confirmation_window
from .select_product import category_window, subcategory_window, product_window
from ..api import ProductsAPI

products_dialog = Dialog(
    category_window,
    subcategory_window,
    product_window,
    set_count_window,
    confirmation_window,
)

register_middlewares(
    router=products_dialog,
    middlewares=ContextMiddleware(
        api=ProductsAPI(
            local_url="http://localhost:8111",
            global_url="https://b40a-185-57-28-68.ngrok-free.app",
        )
    )
)
