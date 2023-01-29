"""Person of the day game handlers: registration, run the game, player rankings and etc."""
from datetime import datetime, timezone

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.services import potd
from bot.services.potd import PersonOfTheDayGame, PersonOfTheDayPlayer


def validate_game(handler):
    """
    Validates if game exists for the current chat.
    Otherwise, sends a message about no players registered.
    """

    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        game = await PersonOfTheDayGame.get(chat.id)
        if not game:
            await context.bot.send_message(
                chat_id=chat.id, text="В этом чате нет зарегистрированных участников!"
            )
            return
        await handler(update, context)

    return wrapped


async def register_player(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Adds new player to the game in the current chat.
    If the game does not exists, then new game with the user will be created.
    Otherwise, user will be added to the existing game.
    """
    user = update.effective_user
    chat = update.effective_chat
    game = await PersonOfTheDayGame.get(chat.id)
    if game is None:
        game = PersonOfTheDayGame(
            id=chat.id, players=[], creation_date=datetime.now(timezone.utc)
        )
    if potd.is_game_has_player(game, user.id):
        await update.message.reply_text(text="Ты уже в игре!")
        return
    else:
        game.players.append(PersonOfTheDayPlayer.from_telegram_user(user=user))
    await game.save()
    await context.bot.send_message(
        chat_id=chat.id,
        text=f"Ты зарегистрирован в игре! Участников игры в этом чате: <b>{len(game.players)}</b>",
        parse_mode=ParseMode.HTML,
    )


@validate_game
async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Lists all players for the game in the current chat.
    """
    chat = update.effective_chat
    game = await PersonOfTheDayGame.get(chat.id)
    await context.bot.send_message(
        chat_id=chat.id,
        text=potd.format_players_to_html_list(game.players),
        parse_mode=ParseMode.HTML,
    )


@validate_game
async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Play game and find a winner: random player from players list.
    """
    chat = update.effective_chat
    game = await PersonOfTheDayGame.get(chat.id)
    if potd.is_game_played_today(game):
        last_winner = potd.get_last_winner(game)
        text = (
            f"Сегодня удача уже улыбнулась {potd.format_player_mention_html(last_winner)}!",
            "<b>Хорошего дня!</b>",
        )
        await context.bot.send_message(
            chat_id=chat.id, text=text, parse_mode=ParseMode.HTML
        )
    else:
        winner = await potd.find_winner(game)
        text = (
            f"Сегодня удачный день будет у {potd.format_player_mention_html(winner)}!",
            "<b>Поздравляем счастливчика!</b>",
        )
        await context.bot.send_message(
            chat_id=chat.id, text=text, parse_mode=ParseMode.HTML
        )
