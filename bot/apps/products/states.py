from aiogram.fsm.state import StatesGroup, State


class ProductFSM(StatesGroup):
    category = State()
    subcategory = State()
    product = State()
