from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.expression import null


# TABLE
class Base(DeclarativeBase):
    pass


class Cards(Base):
    __tablename__ = "card_list"

    card_id = Column(Integer, default=None, primary_key=True, nullable=True)
    # card_name = Column(String(20))
    card_description = Column(String(100))
    is_exploding_kitten = Column(Boolean(100), default=False)
    is_zombie_kitten = Column(Boolean(100), default=False)
    card_effect = Column(String(200))
