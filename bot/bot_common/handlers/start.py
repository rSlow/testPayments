import logging

from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import User
from aiogram_dialog import DialogManager, StartMode, Window, Dialog, ShowMode
from aiogram_dialog.widgets.kbd import Column, Button, Start, Url
from aiogram_dialog.widgets.text import Const
from aiohttp import ClientSession, ClientConnectorError

from bot_config import settings
from ..FSM.single_factory import StartFSM
from ..api import UserAPI

from ..services.subscription import is_subscribed_to
from bot_apps.products.states import ProductFSM

start_router = Router(name="start")


@start_router.message(Command("start"))
async def start(_: types.Message,
                user_api: UserAPI,
                session: ClientSession,
                event_from_user: User,
                dialog_manager: DialogManager):
    user_id = event_from_user.id
    try:
        await user_api.get_user(
            session=session,
            user_id=user_id
        )
        await dialog_manager.start(
            state=StartFSM.state,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.SEND
        )
    except ClientConnectorError:
        logging.warning(f"no user with {user_id = }")


async def check_subscribe(user_id: int,
                          bot: Bot):
    subscribes_to_check = [settings.GROUP_SUBSCRIBE_ID, settings.CHANNEL_SUBSCRIBE_ID]
    subscribed = all([await is_subscribed_to(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id
    ) for chat_id in subscribes_to_check])
    return subscribed


async def start_getter(bot: Bot,
                       event_from_user: User,
                       **__):
    user_id = event_from_user.id
    subscribed = await check_subscribe(
        user_id=user_id,
        bot=bot
    )
    return {
        "subscribed": subscribed,
        "not_subscribed": not subscribed
    }


async def on_subscribed_click(_: types.CallbackQuery,
                              __: Button,
                              manager: DialogManager):
    data = manager.middleware_data
    bot: Bot = data["bot"]
    user: User = data["event_from_user"]
    subscribed = await check_subscribe(
        user_id=user.id,
        bot=bot
    )
    await manager.update({
        "subscribed": subscribed,
        "not_subscribed": not subscribed
    })


start_dialog = Dialog(
    Window(
        Const(
            text="Выберите действие:",
            when="subscribed"
        ),
        Column(
            Start(
                text=Const("Каталог"),
                id="catalog",
                state=ProductFSM.category
            ),
            # Start(
            #     text=Const("Корзина"),
            #     id="cart",
            #     state=...
            # ),
            when="subscribed"
        ),
        Const(
            "Необходимо подписаться на следующие каналы и группы:",
            when="not_subscribed"
        ),
        Column(
            Url(
                text=Const("Канал"),
                url=Const("https://t.me/rs1ow_test")
            ),
            Url(
                text=Const("Группа"),
                url=Const("https://t.me/rslow_test_1")
            ),
            Button(
                text=Const("Я подписался ✅"),
                on_click=on_subscribed_click,
                id="subscribed"
            ),
            when="not_subscribed"
        ),
        getter=start_getter,
        state=StartFSM.state
    ),
)
