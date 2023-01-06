import logging
import os
import random

from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Privet!')

async def select_aboba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text='@' + user.username)


if __name__ == '__main__':
    application = ApplicationBuilder().token(
        os.environ.get('TELEGRAM_TOKEN')).build()
    start_handler = CommandHandler('start', start)
    aboba_handler = CommandHandler('select_aboba', select_aboba)
    application.add_handler(start_handler)
    application.add_handler(aboba_handler)
    application.run_polling()
