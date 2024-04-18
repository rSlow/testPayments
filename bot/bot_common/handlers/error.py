import logging

from aiogram import Router, types
from aiogram_dialog import DialogManager, StartMode, ShowMode

from bot_common.FSM.single_factory import StartFSM

error_router = Router(name="error")


@error_router.error()
async def key_error_pass(event: types.ErrorEvent,
                         dialog_manager: DialogManager):
    # message = event.update.message if event.update.message is not None else event.update.callback_query.message
    # await message.answer(
    #     text=f"Извините, во время работы бота произошла ошибка. Мы вынуждены вернуть вас на главный экран. "
    #          f"Попробуйте воспользоваться функцией еще раз."
    # )
    logging.exception(event.exception)
    # await dialog_manager.start(
    #     state=StartFSM.state,
    #     mode=StartMode.RESET_STACK,
    #     show_mode=ShowMode.SEND
    # )
