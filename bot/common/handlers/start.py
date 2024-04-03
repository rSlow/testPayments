from aiogram import Router, types, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.config import settings
from .. import text
from ..FSM.single_factory import StartFSM
from ..keyboards.main_button import MAIN_BUTTON_DATA
from ..keyboards.start import get_start_keyboard, get_subscription_keyboard

from ..services.subscription import is_subscribed_to
from bot.config.middlewares.current_message import DeleteMarkupCallback

start_router = Router(name="start")


@start_router.message(Command("start"))
@start_router.callback_query(F.data == MAIN_BUTTON_DATA)
async def main(event: types.Message | types.CallbackQuery,
               state: FSMContext,
               bot: Bot,
               delete_markup_callback: DeleteMarkupCallback):
    if isinstance(event, types.Message):
        message = event
    elif isinstance(event, types.CallbackQuery):
        message = event.message
    else:
        raise RuntimeError(f"unknown type of event `{event}`")

    user_id = message.from_user.id
    subscribes_to_check = [settings.GROUP_SUBSCRIBE_ID, settings.CHANNEL_SUBSCRIBE_ID]
    if all([await is_subscribed_to(
            bot=bot,
            chat_id=chat_id,
            user_id=user_id
    ) for chat_id in subscribes_to_check]):
        await state.set_state(StartFSM.state)
        await delete_markup_callback()
        return await message.answer(
            text=text.SELECT_ACTION,
            reply_markup=get_start_keyboard()
        )
    else:
        return await message.answer(
            text="Необходимо подписаться на следующие каналы и группы:",
            reply_markup=get_subscription_keyboard()
        )
