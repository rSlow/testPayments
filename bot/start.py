from bot.config.bot import dispatcher, bot
from bot.config.shutdown import on_shutdown
from bot.config.startup import on_startup

if __name__ == '__main__':
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher.run_polling(bot)
