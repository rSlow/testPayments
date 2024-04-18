from operator import itemgetter

from aiogram import types
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Column, Button, Next, Group
from aiogram_dialog.widgets.media import StaticMedia, MediaScroll
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiohttp import ClientSession

from bot_common.services.whenable import WhenAble
from ..states import ProductFSM
from bot_common.keyboards.buttons import BACK_BUTTON, CANCEL_BUTTON
from bot_common.keyboards.scroll import PagerScroll
from bot_common.types import MediaScrollFormat
from ..api import ProductsAPI


async def category_getter(session: ClientSession,
                          product_api: ProductsAPI,
                          **__):
    categories = await product_api.get_categories(session)
    return {'categories': [(category.name, category.pk) for category in categories]}


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


async def subcategory_getter(dialog_manager: DialogManager,
                             session: ClientSession,
                             product_api: ProductsAPI,
                             **__):
    category_id = dialog_manager.dialog_data.get("category_id")
    category = await product_api.get_category(
        session=session,
        category_id=category_id
    )
    return {
        "current_category": category,
        "subcategories": [(subcategory.name, subcategory.pk) for subcategory in category.subcategories]
    }


async def on_subcategory_click(_: types.CallbackQuery,
                               __: Button,
                               manager: DialogManager,
                               data: int):
    manager.dialog_data.update(subcategory_id=data)
    await manager.next()


subcategory_window = Window(
    Format("Текущая категория: {current_category.name}"),
    Const(
        text="Выберите подкатегорию:",
        when="subcategories"
    ),
    Const(
        text="В этой категории нет товаров :(",
        when=~WhenAble("subcategories")
    ),
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
        id="subcategory_scroll",
        when="subcategories"
    ),
    BACK_BUTTON,
    getter=subcategory_getter,
    state=ProductFSM.subcategory
)


async def product_getter(dialog_manager: DialogManager,
                         session: ClientSession,
                         product_api: ProductsAPI,
                         **__):
    current_page: int = await dialog_manager.find(MEDIA_SCROLL).get_page()
    dialog_data = dialog_manager.dialog_data
    subcategory_id = dialog_data.get("subcategory_id")

    subcategory = await product_api.get_subcategory(
        session=session,
        subcategory_id=subcategory_id,
        local=False
    )
    products = subcategory.products
    data = {
        'products': products,
        "current_subcategory": subcategory
    }
    if products:
        product = products[current_page]
        data.update({"product": product})
        dialog_data.update({"product_id": product.pk})
    return data


MEDIA_SCROLL = "media_scroll"
product_window = Window(
    Const(
        text="В этой подкатегории нет товаров :(",
        when=~WhenAble("products")
    ),
    Multi(
        Format("<b>{product.title}</b>"),
        Format("{product.description}"),
        sep="\n\n",
        when="product"
    ),
    MediaScroll(
        media=StaticMedia(url=MediaScrollFormat("{product.photo}")),
        items="products",
        id=MEDIA_SCROLL,
        when="product"
    ),
    Group(
        PagerScroll(MEDIA_SCROLL),
        Column(
            Next(
                text=Format("Добавить в корзину 🧺"),
                id="add_on_cart",
            )
        ),
        when="product"
    ),
    BACK_BUTTON,
    getter=product_getter,
    state=ProductFSM.product
)
