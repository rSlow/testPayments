from aiogram_dialog import Dialog

from .add_product import set_count_window, confirmation_window
from .select_product import category_window, subcategory_window, product_window

products_dialog = Dialog(
    category_window,
    subcategory_window,
    product_window,
    set_count_window,
    confirmation_window,
)
