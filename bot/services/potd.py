from datetime import datetime, timezone
from typing import Iterable, List, Optional

from beanie import Document
from pydantic import BaseModel
from telegram import User


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
        return cls(id=user.id,
                   username=user.username,
                   first_name=user.first_name,
                   last_name=user.last_name,
                   wins_number=0)


class PersonOfTheDayGame(Document):
    """
    Person of the day game.
    ID is the Telegram chat ID, so only one game per chat allowed.
    """
    id: int
    players: List[PersonOfTheDayPlayer]
    last_winner_id: Optional[int] = None
    last_play_date: datetime
    creation_date: datetime

    class Settings:
        name = "potd"


def get_player_name_for_mention(player: PersonOfTheDayPlayer) -> str:
    """
    Returns username for mention if exists, otherwise returns first name.
    """
    return player.username if player.username else player.first_name


def is_game_has_player(game: PersonOfTheDayGame) -> bool:
    """
    Returns true if player with the given ID is in the game, othewise false.
    """
    return any(player.id == id for player in game.players)


def is_game_played_today(game: PersonOfTheDayGame) -> bool:
    """
    Returns true if game is already played today, othewise false.
    """
    return game.last_play_date.date() == datetime.now(timezone.utc).date()


def format_players_to_html_list(players: Iterable[PersonOfTheDayPlayer]) -> str:
    return ""
