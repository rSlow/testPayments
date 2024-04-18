from aiogram import Dispatcher, Bot


async def on_shutdown(dispatcher: Dispatcher,
                      bot: Bot):
    await bot.session.close()
