from datetime import datetime, timezone
from typing import List

from telegram import Update
from telegram.ext import ContextTypes

from bot.services.potd import PersonOfTheDayGame, PersonOfTheDayPlayer


async def register_player(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Adds new player to the game in the current chat. 
    If the game does not exists, then new game with the user will be created.
    Otherwise, user will be added to the existing game.
    """
    user = update.effective_user
    chat = update.effective_chat
    potd_game = await PersonOfTheDayGame.get(chat.id)
    if potd_game is None:
        potd_game = PersonOfTheDayGame(id=chat.id, players=[], last_play_date=datetime.now(
            timezone.utc), creation_date=datetime.now(timezone.utc))
    if potd_game.has_player(user.id):
        await update.message.reply_text(text='Ты уже в игре!')
        return
    else:
        potd_game.players.append(
            PersonOfTheDayPlayer.from_telegram_user(user=user))
    await potd_game.save()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=_format_registered_msg(potd_game))


async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Lists all players for the game in the current chat.
    """
    chat = update.effective_chat
    potd_game = await PersonOfTheDayGame.get(chat.id)
    if potd_game:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Участники игры в этом чате:\n' + _format_players_list(potd_game.get_player_list()))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='В этом чате нет зарегистрированных участников!')


def _format_registered_msg(potd_game: PersonOfTheDayGame) -> str:
    return "Ты зарегистрирован в игре! Участников игры в этом чате: {}".format(len(potd_game.players))


# def _format_players_list(players: List[PersonOfTheDayPlayer]) -> str:

#     formatted_players = "{}. {}".format(i + 1, player.get_name_for_mention()) for i, player in enumerate(players)
#     return '\n'.join()


# def stats_to_str(list):
#     return '\n'.join("{0}. {1} ({2}) - {3}".format(idx + 1, p.id, p.get_name(), p.wins_number) for idx, p in enumerate(list))


# async def list_winners_for_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     chat = update.effective_chat
#     potd_game = await PersonOfTheDayGame.get(chat.id)

#     if (potd_game):
#         winners_list = sorted(potd_game.get_player_list(),
#                               key=lambda p: p.wins_number, reverse=True)
#         await context.bot.send_message(chat_id=update.effective_chat.id, text='Результаты:\n' + stats_to_str(winners_list))


# async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user = update.effective_user
#     chat = update.effective_chat
#     potd_game = await PersonOfTheDayGame.get(chat.id)

#     if potd_game:
#         if potd_game.play_allowed():
#             winner_id = await potd_game.play()
#             winner_user = next(
#                 filter(lambda p: p.id == winner_id, potd_game.get_player_list()))

#             await context.bot.send_message(chat_id=update.effective_chat.id, text='Поздравляем {0}. Ты сегодня пидор!'.format(helpers.mention_html(winner_id, winner_user.get_name())), parse_mode='HTML')
#         else:
#             if (potd_game.last_winner_id):
#                 winner_user = next(
#                     filter(lambda p: p.id == potd_game.last_winner_id, potd_game.get_player_list()))
#                 await update.message.reply_text(text='Иди нахуй, игра закончена! Сегодня пидор {0}'.format(helpers.mention_html(winner_user.id, winner_user.get_name())), parse_mode='HTML')