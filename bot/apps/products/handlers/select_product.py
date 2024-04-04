from operator import itemgetter

from aiogram import types
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Column, Button, Next
from aiogram_dialog.widgets.media import StaticMedia, MediaScroll
from aiogram_dialog.widgets.text import Const, Format, Multi

from bot.apps.products.states import ProductFSM
from api.apps.products.models import Category, SubCategory, Product
from bot.common.keyboards.buttons import BACK_BUTTON, CANCEL_BUTTON
from bot.common.keyboards.scroll import PagerScroll
from bot.common.types import MediaScrollFormat


async def category_getter(**__):
    categories: list[tuple[str, int]] = [
        (category.name, category.pk)
        async for category in Category.objects.all()
    ]
    return {'categories': categories}


async def on_category_click(_: types.CallbackQuery,
                            __: Button,
                            manager: DialogManager,
                            data: int):
    manager.dialog_data.update(category_id=data)
    await manager.next()


category_window = Window(
    Const("Выберите категорию товара:"),
    ScrollingGroup(
        Column(
            Select(
                Format("{item[0]}"),
                items="categories",
                item_id_getter=itemgetter(1),
                id="category_select",
                on_click=on_category_click
            )
        ),
        height=4,
        id="category_scroll"
    ),
    CANCEL_BUTTON,
    getter=category_getter,
    state=ProductFSM.category
)


async def subcategory_getter(dialog_manager: DialogManager, **__):
    category_id = dialog_manager.dialog_data.get("category_id")
    subcategories: list[tuple[str, int]] = [
        (subcategory.name, subcategory.pk)
        async for subcategory in SubCategory.objects.filter(category_id=category_id)
    ]
    return {
        'subcategories': subcategories
    }


async def on_subcategory_click(_: types.CallbackQuery,
                               __: Button,
                               manager: DialogManager,
                               data: int):
    manager.dialog_data.update(subcategory_id=data)
    await manager.next()


subcategory_window = Window(
    Const("Выберите подкатегорию:"),
    ScrollingGroup(
        Column(
            Select(
                Format("{item[0]}"),
                items="subcategories",
                item_id_getter=itemgetter(1),
                id="subcategory_select",
                on_click=on_subcategory_click
            )
        ),
        height=4,
        id="subcategory_scroll"
    ),
    BACK_BUTTON,
    getter=subcategory_getter,
    state=ProductFSM.subcategory
)


async def product_getter(dialog_manager: DialogManager, **__):
    current_page: int = await dialog_manager.find(MEDIA_SCROLL).get_page()
    dialog_data = dialog_manager.dialog_data
    category_id = dialog_data.get("category_id")
    subcategory_id = dialog_data.get("subcategory_id")

    products: list[Product] = [
        product async for product in Product.objects.filter(
            subcategory_id=subcategory_id,
            subcategory__category_id=category_id
        )
    ]
    data = {'products': products}
    if products:
        product: Product = products[current_page]
        data.update({"product": product})
        dialog_data.update({"product_id": product.id})
    return data


def no_products(data: dict, *_):
    return not data.get("products")


MEDIA_SCROLL = "media_scroll"
product_window = Window(
    Const(
        text="В этой подкатегории нет товаров :(",
        when=no_products
    ),
    Multi(
        Format("<b>{product.title}</b>"),
        Format("{product.description}"),
        sep="\n\n",
        when="product"
    ),
    MediaScroll(
        media=StaticMedia(path=MediaScrollFormat("{product.photo.path}")),
        items="products",
        id=MEDIA_SCROLL,
        when="product",
    ),
    PagerScroll(
        MEDIA_SCROLL,
        when="product"
    ),
    Column(
        Next(
            text=Format("Добавить в корзину 🧺"),
            id="add_on_cart",
        ),
        BACK_BUTTON
    ),
    getter=product_getter,
    state=ProductFSM.product
)
