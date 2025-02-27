from sqlalchemy import Column, Integer, String, Boolean, ARRAY
from sqlalchemy.orm import DeclarativeBase


# TABLE
class Base(DeclarativeBase):
    pass


class Cards(Base):
    __tablename__ = "card_list"

    card_id = Column(Integer, default=None, primary_key=True, nullable=True)
    card_name = Column(String(20))
    card_description = Column(String(100))
    is_exploding_kitten = Column(Boolean)
    is_zombie_kitten = Column(Boolean)
    card_type = Column(String(200))
    img_path = Column(String(200))
    is_now = Column(Boolean)
    with_cat_paw = Column(Integer)
    card_count = Column(Integer)


class Deck(Base):
    __tablename__ = "current_deck"

    current_deck_id = Column(Integer, default=None,
                             primary_key=True, nullable=True)
    lobby_id = Column(Integer)
    card_array = Column(ARRAY(Integer), nullable=True)
    discard_array = Column(ARRAY(Integer), nullable=True)
    zombie_kitten_count = Column(Integer)
    exploding_kitten_count = Column(Integer)
