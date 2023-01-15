import logging
from asyncio import get_event_loop, new_event_loop, set_event_loop

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import config
from database import database, mongodb

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

loop.run_until_complete((mongodb.check_connection(config.MONGO_URI)))


async def save_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await database.save_user(update.effective_user)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я сохранил тебя в базу данных!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', save_user)
    application.add_handler(start_handler)
    application.run_polling()
