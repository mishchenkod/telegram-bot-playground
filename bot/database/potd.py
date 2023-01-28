from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel


class PersonOfTheDayPlayer(BaseModel):
    '''
    Person of the day game participant.
    '''
    id: int
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

    def is_player_exist(self, user_id: int) -> bool:
        return any(player.id == user_id for player in self.players)

    async def add_player(self, user) -> bool:
        player_added = False
        if not self.is_player_exist(user.id):
            potd_player: PersonOfTheDayPlayer = PersonOfTheDayPlayer(id =           user.id, 
                                                                    username =      user.username, 
                                                                    first_name =    user.first_name, 
                                                                    last_name =     user.last_name, 
                                                                    wins_number =   0)
            self.players.append(potd_player)
            await self.save()
            player_added = True
        return player_added

    def get_player_list(self) -> List:
        return self.players


    class Settings:
        name = "potd"
