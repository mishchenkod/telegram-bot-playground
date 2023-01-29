"""Person of the day game service"""
from datetime import datetime, timezone
from typing import Iterable, List, Optional

from beanie import Document
from numpy import random
from pydantic import BaseModel
from telegram import User, helpers


class PersonOfTheDayPlayer(BaseModel):
    """
    Person of the day game participant.
    """

    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    wins_number: int

    @classmethod
    def from_telegram_user(cls, user: User):
        """
        Creates player instance from Telegram user.
        """
        return cls(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            wins_number=0,
        )


class PersonOfTheDayGame(Document):
    """
    Person of the day game.
    ID is the Telegram chat ID, so only one game per chat allowed.
    """

    id: int
    players: List[PersonOfTheDayPlayer]
    last_winner_id: Optional[int] = None
    last_play_date: Optional[datetime] = None
    creation_date: datetime

    class Settings:
        """Collection settings"""

        name = "potd"


async def find_winner(game: PersonOfTheDayGame) -> PersonOfTheDayPlayer:
    """
    Finds game winner and updates last played date.
    """
    winner = random.choice(game.players)
    winner.wins_number += 1
    game.last_winner_id = winner.id
    game.last_play_date = datetime.now(timezone.utc)
    await game.save()
    return winner


def get_last_winner(game: PersonOfTheDayGame) -> PersonOfTheDayPlayer:
    """
    Returns last winnner player.
    """
    return next(
        (player for player in game.players if player.id == game.last_winner_id), None
    )


def is_game_has_player(game: PersonOfTheDayGame, player_id: int) -> bool:
    """
    Returns true if player with the given ID is in the game, othewise false.
    """
    return any(player.id == player_id for player in game.players)


def is_game_played_today(game: PersonOfTheDayGame) -> bool:
    """
    Returns true if game is already played today, othewise false.
    """
    return (
        False
        if (game.last_play_date is None)
        else (game.last_play_date.date() == datetime.now(timezone.utc).date())
    )


def format_players_to_html_list(players: Iterable[PersonOfTheDayPlayer]) -> str:
    """
    Returns HTML-formatted numbered list of players sorted by wins number.
    """
    sorted_players = sorted(players, key=lambda p: p.wins_number, reverse=True)
    formatted_players = ["<b>Рейтинг счастливчиков:</b>\n"]
    for index, player in enumerate(sorted_players):
        formatted_players.append(
            (
                f"{index + 1}. {format_player_mention_html(player)} "
                f"({player.wins_number} счастливых дней)\n"
            )
        )
    return "".join(formatted_players)


def format_player_mention_html(player: PersonOfTheDayPlayer) -> str:
    """
    Returns HTML-formatted Telegram mention.
    """
    return helpers.mention_html(player.id, _get_player_name_for_mention(player))


def _get_player_name_for_mention(player: PersonOfTheDayPlayer) -> str:
    """
    Returns username for mention if exists, otherwise returns first name.
    """
    return player.username if player.username else player.first_name
