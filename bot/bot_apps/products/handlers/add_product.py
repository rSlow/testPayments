from aiogram import types
from aiogram.types import User
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Counter, Row, Back
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const, Multi
from aiohttp import ClientSession

from bot_common.api import UserAPI
from bot_common.keyboards.buttons import BACK_BUTTON
from ..api import ProductsAPI
from ..states import ProductFSM


async def count_getter(dialog_manager: DialogManager,
                       session: ClientSession,
                       product_api: ProductsAPI,
                       **__):
    product_id: int = dialog_manager.dialog_data.get("product_id")
    product = await product_api.get_product(
        session=session,
        product_id=product_id,
        local=False
    )
    return {"product": product}


async def on_add_in_cart(_: types.CallbackQuery,
                         __: Button,
                         manager: DialogManager):
    product_count: float = manager.find(COUNTER_ID).get_value()
    manager.dialog_data.update({"product_count": product_count})
    await manager.next()


COUNTER_ID = "product_counter"

set_count_window = Window(
    StaticMedia(url=Format("{product.photo}")),
    Format("<b>{product.title}</b>"),
    Counter(
        id=COUNTER_ID,
        default=1,
    ),
    Button(
        text=Const("Добавить в корзину 🧺"),
        id="add_on_cart",
        on_click=on_add_in_cart
    ),
    BACK_BUTTON,
    state=ProductFSM.set_count,
    getter=count_getter,
)


async def confirmation_getter(dialog_manager: DialogManager,
                              session: ClientSession,
                              product_api: ProductsAPI,
                              **__):
    dialog_data = dialog_manager.dialog_data
    product_id = dialog_data.get("product_id")
    product_count = dialog_data.get("product_count")
    product = await product_api.get_product(
        session=session,
        product_id=product_id
    )
    return {
        "product": product,
        "product_count": product_count
    }


async def on_confirm(_: types.CallbackQuery,
                     __: Button,
                     manager: DialogManager):
    middleware_data = manager.middleware_data
    product_api: ProductsAPI = middleware_data["product_api"]
    user_api: UserAPI = middleware_data["user_api"]
    session: ClientSession = middleware_data["session"]
    product_count = manager.dialog_data["product_count"]
    product_id = manager.dialog_data["product_id"]

    user: User = middleware_data["event_from_user"]
    user_model = await user_api.get_user(
        session=session,
        user_id=user.id
    )
    cart = await product_api.get_cart(
        session=session,
        user_id=user_model.pk
    )
    # await product_api.add_product_in_cart(
    #     session=session,
    #     product_id=product_id,
    #     cart_id=cart.pk,
    #     count=product_count
    # )


confirmation_window = Window(
    Multi(
        Const("Подтверждаем:"),
        Format("<b>Товар</b>: {product.title}"),
        Format("<b>Количество</b>: {product_count}")
    ),
    Row(
        Button(
            Const("Да"),
            on_click=on_confirm,
            id="confirm"
        ),
        Back(Const("Нет"))
    ),
    state=ProductFSM.confirmation,
    getter=confirmation_getter
)
