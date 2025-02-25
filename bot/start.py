from bot_config.bot import dispatcher, bot
from bot_config.shutdown import on_shutdown
from bot_config.startup import on_startup

if __name__ == '__main__':
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher.run_polling(bot)
