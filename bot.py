import datetime
import logging
from asyncio import get_event_loop, new_event_loop, set_event_loop
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from bot.config import config
from bot.database import mongo
from bot.models.chat_user import ChatUser

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

loop.run_until_complete((mongo.check_connection(config.MONGO_URI)))
loop.run_until_complete((mongo.initialize()))


async def start_greetings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Я бот после CI/CD')


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    logger.info(user)
    chat_user = ChatUser(user_id=user.id, chat_id=chat.id, username=user.username,
                         first_name=user.first_name, last_name=user.last_name, last_update=datetime.now(timezone.utc))
    await chat_user.insert()
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Пользователь зарегистрирован: ' + str(chat_user))


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start_greetings)
    register_user_handler = CommandHandler('register', register_user)
    application.add_handler(start_handler)
    application.add_handler(register_user_handler)
    application.run_polling()
