from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_keyboard():
    catalog = InlineKeyboardButton(
        text="Каталог",
        callback_data="catalog"
    )
    cart = InlineKeyboardButton(
        text="Корзина",
        callback_data="cart"
    )
    builder = InlineKeyboardBuilder().add(
        catalog, cart
    ).adjust(1)
    return builder.as_markup()


def get_subscription_keyboard():
    channel = InlineKeyboardButton(
        text='Канал',
        url='https://t.me/rs1ow_test'
    )
    group = InlineKeyboardButton(
        text='Группа',
        url='https://t.me/rslow_test_1'
    )
    subscribed = InlineKeyboardButton(
        text='Я подписался ✅',
        callback_data="subscribed"
    )
    builder = InlineKeyboardBuilder().add(
        channel, group, subscribed
    ).adjust(1)
    return builder.as_markup()
