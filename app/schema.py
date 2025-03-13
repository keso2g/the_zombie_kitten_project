from typing import Optional, Annotated
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field, model_validator, ConfigDict


class CardList(BaseModel):
    card_id: Optional[int]
    card_name: str
    card_description: str
    is_exploding_kitten: bool
    is_zombie_kitten: bool
    card_type: str
    img_path: str
    is_now: bool
    with_cat_paw: int
    card_count: int

    class Config:
        from_attributes = True


class CurrentDeck(BaseModel):
    current_deck_id: int
    lobby_id: int
    card_array: list
    discard_array: list
    zombie_kitten_count: int
    exploding_kitten_count: int

    class Config:
        from_attributes = True


class Lobby(BaseModel):
    lobby_id: int
    player_id: int
    lobby_code: str
    lobby_pass: str
    date_created: Optional[datetime]
    date_ended: Optional[datetime]
    turn_order: int
    is_active: bool

    class Config:
        from_attributes = True


class PlayBox(BaseModel):
    session_id: int
    player_id: int
    lobby_id: int
    current_turn_order: int
    is_player_dead: bool
    hand_card_array: list

    class Config:
        from_attributes = True


class PlayerInfo(BaseModel):
    player_id: int
    player_uuid: str = Field(max_length=255)
    username: str = Field(max_length=20)
    password: str = Field(min_length=8, max_length=15)
    player_name: str = Field(min_length=8, max_length=30)
    wins: int
    loss: int
    games_played: int

    class Config:
        from_attributes = True
