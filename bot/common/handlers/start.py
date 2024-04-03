from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..keyboard import get_start_keyboard, get_subscription_keyboard

from ..services.subscription import is_subscribed_to_group, is_subscribed_to_channel

start_router = Router(name="start")


@start_router.message(Command("start"))
async def start(message: types.Message,
                state: FSMContext):
    subscribed_to_group = await is_subscribed_to_group()
    subscribed_to_channel = await is_subscribed_to_channel()

    if subscribed_to_group and subscribed_to_channel:
        await message.answer(
            text="Куда надо?",
            reply_markup=get_start_keyboard()
        )
    else:
        await message.answer(
            text="Куда надо?",
            reply_markup=get_subscription_keyboard()
        )
