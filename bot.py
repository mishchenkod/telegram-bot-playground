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
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Ты зарегистрирован в игре!')
    else:
        await update.message.reply_text(text='Ты уже зарегистрирован в игре, иди нахуй!')

def players_to_str(list) -> str:
    return '\n'.join("{0}. {1} ({2})".format(idx + 1, p.id, p.get_name()) for idx, p in enumerate(list))

async def list_players_for_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    potd_game = await PersonOfTheDayGame.get(chat.id)
    if (potd_game):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Участники игры в этом чате:\n' + players_to_str(potd_game.get_player_list()))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='В этом чате нет игры!')

async def list_winners_for_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return

##############################################################################################################################################################

def get_handlers() -> dict[str, callable]:
    handlers: dict[str, callable] = {
        'start': start_greetings,
        'register': register_potd,
        'players': list_players_for_game,
        'winners': list_winners_for_game
    }

    return handlers

def add_handlers(application) -> None:
    for command_name, handler in get_handlers().items():
        application.add_handler(CommandHandler(command_name, handler))

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    add_handlers(application)
    application.run_polling()
