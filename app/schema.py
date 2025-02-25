from typing import Optional
from pydantic import BaseModel


class CardSchema(BaseModel):
    card_id: Optional[int]
    # card_name: str
    card_description: str
    is_exploding_kitten: bool
    is_zombie_kitten: bool
    card_effect: str

    class Config:
        from_attributes = True
