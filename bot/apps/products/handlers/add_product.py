from aiogram import types
from aiogram.types import User
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Counter, ManagedCounter, Row, Back
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const, Multi

from api.apps.products.models import Product
from api.apps.user.models import User as ModelUser
from bot.common.keyboards.buttons import BACK_BUTTON
from ..states import ProductFSM


async def count_getter(dialog_manager: DialogManager, **__):
    product_id: int = dialog_manager.dialog_data.get("product_id")
    product: Product = await Product.objects.aget(id=product_id)
    return {
        "product": product
    }


async def on_add_in_cart(_: types.CallbackQuery,
                         __: Button,
                         manager: DialogManager):
    counter: ManagedCounter = manager.find(COUNTER_ID)
    product_count = counter.get_value()
    manager.dialog_data.update({"product_count": product_count})
    await manager.next()


COUNTER_ID = "product_counter"

set_count_window = Window(
    StaticMedia(path=Format("{product.photo.path}")),
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


async def confirmation_getter(dialog_manager: DialogManager, **__):
    dialog_data = dialog_manager.dialog_data
    product_id = dialog_data.get("product_id")
    product_count = dialog_data.get("product_count")
    product = await Product.objects.aget(id=product_id)
    return {
        "product": product,
        "product_count": product_count
    }


async def on_confirm(_: types.CallbackQuery,
                     __: Button,
                     manager: DialogManager):
    middleware_data = manager.middleware_data
    user: User = middleware_data["event_from_user"]
    ModelUser.objects.aget_or_create()


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
