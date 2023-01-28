import datetime
import logging
from asyncio import get_event_loop, new_event_loop, set_event_loop
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from bot.config import config
from bot.database.mongo import initialize_database
from bot.database.potd import PersonOfTheDayGame, PersonOfTheDayPlayer

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


async def start_greetings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Я бот после CI/CD')

async def get_game(chat_id: int) -> PersonOfTheDayGame:
    potd_game = await PersonOfTheDayGame.get(chat_id)
    if potd_game is None:
        potd_game = PersonOfTheDayGame(id=chat_id, players=[], last_play_date=datetime.now(timezone.utc), creation_date=datetime.now(timezone.utc))

    return potd_game

async def register_potd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat

    potd_game = await get_game(chat.id)

    if await potd_game.add_player(user):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Ты зарегистрирован в игре: ' + str(potd_game))
    else:
        await update.message.reply_text(text='Ты уже зарегистрирован в игре, иди нахуй!')

async def list_players_for_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    potd_game = await PersonOfTheDayGame.get(chat.id)
    if (potd_game):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Участники игры в этом чате: ' + str(potd_game))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='В этом чате нет игры!')


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start_greetings)
    register_potd_handler = CommandHandler('register', register_potd)
    list_potd_handler = CommandHandler('list', list_players_for_game)
    application.add_handler(start_handler)
    application.add_handler(register_potd_handler)
    application.add_handler(list_potd_handler)
    application.run_polling()
