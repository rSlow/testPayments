from config.bot import dispatcher, bot
from config.shutdown import on_shutdown
from config.startup import on_startup

if __name__ == '__main__':
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher.run_polling(bot)
