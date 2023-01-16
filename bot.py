import logging
from asyncio import get_event_loop, new_event_loop, set_event_loop

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import config
from database import mongo, mongo_users

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


async def start_greetings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Я бот')


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await mongo_users.save_user(update.effective_user)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Я сохранил тебя в базу данных')


async def find_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = int(context.args[0])
        user = await mongo_users.find_user(user_id)
        if not user:
            await update.message.reply_text('Пользователь с таким ID не найден')
        else:
            await update.message.reply_text(str(user))
    except (IndexError, ValueError):
        await update.message.reply_text('Необходимо указать ID пользователя!')


async def get_all_user_ids(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_ids = await mongo_users.get_all_user_ids()
    joined_user_ids = ','.join(map(str, user_ids))
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Все пользователи: ' + joined_user_ids)


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start_greetings)
    register_user_handler = CommandHandler('register', register_user)
    get_all_user_ids_handler = CommandHandler('list_users', get_all_user_ids)
    find_user_handler = CommandHandler('find_user', find_user)
    application.add_handler(start_handler)
    application.add_handler(register_user_handler)
    application.add_handler(get_all_user_ids_handler)
    application.add_handler(find_user_handler)
    application.run_polling()
