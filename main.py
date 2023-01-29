import logging
from asyncio import get_event_loop, new_event_loop, set_event_loop

from telegram.ext import ApplicationBuilder

from bot import config
from bot.database import initialize_database

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger("__name__")

try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

loop.run_until_complete((initialize_database()))


def add_handlers(application) -> None:
    for command_name, handler in get_handlers().items():
        application.add_handler(CommandHandler(command_name, handler))


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    application.run_polling()
