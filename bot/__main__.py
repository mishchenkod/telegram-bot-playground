"""Bot starting, logging configuration and handlers registration"""
import logging
import traceback
from asyncio import get_event_loop, new_event_loop, set_event_loop

from telegram.ext import ApplicationBuilder, CommandHandler

from bot import config
from bot.database import mongo
from bot.handlers import potd_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger("__name__")

try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

loop.run_until_complete((mongo.initialize_database()))


def main():
    """Initialize bot"""
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("register", potd_handler.register_player))
    application.add_handler(CommandHandler("players", potd_handler.list_players))
    application.add_handler(CommandHandler("play", potd_handler.play_game))
    application.run_polling()


try:
    main()
except Exception:
    logger.warning(traceback.format_exc())
