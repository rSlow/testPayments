from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot.apps.products.callback_factory import ProductFactory
from bot.apps.products.states import ProductFSM
from api.apps.products.models import Product
from bot.common.services.inline_select import InlineSelect

product_router = Router(name="product")


@product_router.callback_query(
    ProductFSM.subcategory,
    ProductFactory.filter()
)
async def select_product(callback: types.CallbackQuery,
                         callback_data: ProductFactory,
                         state: FSMContext):
    await state.set_state(ProductFSM.product)
    products: list[Product] = [
        category async for category
        in Product.objects.filter(
            subcategory_id=callback_data.subcategory,
            subcategory__category_id=callback_data.category,
        )]
    select = InlineSelect(
        page_key="current_product_page",
        fsm_context=state,
        on_page=1,
        items=products,
        main_func=select_product,
        main_func_kwargs={"callback_data": callback_data}
    )
    select.add()

    await callback.message.edit_text(
        text="Выберите подкатегорию товара:",
        reply_markup=select.as_markup()
    )
