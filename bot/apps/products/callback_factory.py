from typing import Optional

from aiogram.filters.callback_data import CallbackData


class ProductFactory(CallbackData, prefix="product"):
    category: int
    subcategory: Optional[int] = None
    product: Optional[int] = None
