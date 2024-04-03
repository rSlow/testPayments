import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

error_router = Router(name="error")


@error_router.error()
async def key_error_pass(event: types.ErrorEvent,
                         state: FSMContext):
    data = await state.get_data()
    message = event.update.message if event.update.message is not None else event.update.callback_query.message
    await start(
        message=message,
        state=state,
        text=f"Извините, во время работы бота произошла ошибка. Мы вынуждены вернуть вас на главный экран. "
             f"Попробуйте воспользоваться функцией еще раз."
    )
    logging.exception(event.exception)


