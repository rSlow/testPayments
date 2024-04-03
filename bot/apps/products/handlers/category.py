from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton

from bot.apps.products.callback_factory import ProductFactory
from bot.apps.products.states import ProductFSM
from bot.common.FSM.single_factory import StartFSM
from api.apps.products.models import Category
from bot.common.keyboards.main_button import MAIN_BUTTON
from bot.common.services.inline_select import InlineSelect

category_router = Router(name="category")


def category_factory(item: Category):
    return InlineKeyboardButton(
        text=item.name,
        callback_data=ProductFactory(category=item.pk).pack()
    )


@category_router.callback_query(
    StartFSM.state,
    F.data == "catalog"
)
async def select_category(callback: types.CallbackQuery,
                          state: FSMContext):
    await state.set_state(ProductFSM.category)
    categories: list[Category] = [category async for category in Category.objects.all()]
    select = InlineSelect(
        page_key="current_category_page",
        fsm_context=state,
        on_page=3,
        items=categories,
        factory=category_factory,
        main_func=select_category
    )
    select.register_pagination(
        router=category_router,
        fsm_state=ProductFSM.category,
    )

    await select.paginate()
    select.row(MAIN_BUTTON)
    await callback.message.edit_text(
        text="Выберите категорию товара:",
        reply_markup=select.as_markup()
    )
