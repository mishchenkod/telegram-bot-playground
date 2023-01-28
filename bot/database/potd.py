from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel


class PersonOfTheDayPlayer(BaseModel):
    '''
    Person of the day game participant.
    '''
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    wins_number: int


class PersonOfTheDayGame(Document):
    '''
    Person of the day game.
    ID is the Telegram chat ID, so only one game per chat allowed.
    '''
    id: int
    players: List[PersonOfTheDayPlayer]
    last_winner_id: Optional[int] = None
    last_play_date: datetime
    creation_date: datetime

    class Settings:
        name = "potd"
