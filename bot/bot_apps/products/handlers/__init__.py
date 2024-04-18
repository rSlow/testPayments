from aiogram_dialog import Dialog

from bot_common.middlewares import register_middlewares
from bot_common.middlewares.context import ContextMiddleware
from bot_config import settings
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
