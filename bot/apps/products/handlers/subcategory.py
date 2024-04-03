from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton

from bot.apps.products.callback_factory import ProductFactory
from bot.apps.products.states import ProductFSM
from api.apps.products.models import SubCategory
from bot.common.keyboards.main_button import MAIN_BUTTON
from bot.common.services.inline_select import InlineSelect

subcategory_router = Router(name="subcategory")


def subcategory_factory(item: SubCategory):
    return InlineKeyboardButton(
        text=item.name,
        callback_data=ProductFactory(category=item.pk).pack()
    )


@subcategory_router.callback_query(
    ProductFSM.category,
    ProductFactory.filter()
)
async def select_subcategory(callback: types.CallbackQuery,
                             callback_data: ProductFactory,
                             state: FSMContext):
    await state.set_state(ProductFSM.subcategory)
    subcategories: list[SubCategory] = [
        category async for category
        in SubCategory.objects.filter(category_id=callback_data.category)]
    select = InlineSelect(
        page_key="current_subcategory_page",
        fsm_context=state,
        on_page=3,
        items=subcategories,
        factory=subcategory_factory,
        main_func=select_subcategory,
        main_func_kwargs={"callback_data": callback_data}
    )
    select.register_pagination(
        router=subcategory_router,
        fsm_state=ProductFSM.category,
    )

    await select.paginate()
    select.row(MAIN_BUTTON)

    await callback.message.edit_text(
        text="Выберите подкатегорию товара:",
        reply_markup=select.as_markup()
    )
