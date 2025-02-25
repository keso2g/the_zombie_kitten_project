from fastapi import FastAPI, Response, status, Depends, HTTPException
from sqlalchemy import MetaData, delete, select, update
from sqlalchemy.orm import Session
from .models import Base, Cards
from .database import engine, get_db
from .schema import CardSchema

# META
metadata = MetaData()

# EXECUTE TABLE
Base.metadata.create_all(bind=engine)

app = FastAPI()

session = Session(engine)


# HOME PAGE
@app.get("/")
def home():
    return {"Welcome to the Exploding Kitten Wiki!"}


# VIEW ALL ITEMS
@app.get("/cards/", response_model=list[CardSchema])
def view(db: Session = Depends(get_db)):
    cards = db.query(Cards).order_by(Cards.card_id).all()
    return cards


# ADD AN ITEM
@app.post("/add_card/", response_model=CardSchema, status_code=status.HTTP_201_CREATED)
def add_one(card: CardSchema, db: Session = Depends(get_db)):
    add_card = Cards(card_effect=card.card_effect,
                     card_description=card.card_description,
                     is_exploding_kitten=card.is_exploding_kitten,
                     is_zombie_kitten=card.is_zombie_kitten)
    db.add(add_card)
    db.commit()
    db.refresh(add_card)
    return add_card


# UPDATE A CARD
@app.put("/update_card/{id}", response_model=CardSchema, status_code=status.HTTP_202_ACCEPTED)
def update_card(id: int, card: CardSchema, db: Session = Depends(get_db)):
    id_filter = db.query(Cards).filter(Cards.card_id == id).first()
    if id_filter == None:
        raise HTTPException(
            status_code=404, detail=f"Card ID: {id} not found!")
    id_filter.card_effect = card.card_effect
    id_filter.card_description = card.card_description
    id_filter.is_exploding_kitten = card.is_exploding_kitten
    id_filter.is_zombie_kitten = card.is_exploding_kitten
    db.commit()
    return id_filter

# VIEW AN ITEM


@app.get("/cards/{id}", response_model=CardSchema)
def get_one(id: int, db: Session = Depends(get_db)):
    view = db.query(Cards).filter(Cards.card_id == id).first()
    if not view:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Card ID: {id} not found!")
    return view


# GET CARD USING QUERY PARAMS
@app.get("/cards/", response_model=CardSchema)
def get_one(q: str, values: int = None, db: Session = Depends(get_db)):
    if q:
        if q == "id":
            view = db.query(Cards).filter(Cards.card_id == values).first()
            return (view)
        elif q != "id":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Please use a valid query!")


# DELETE AN ITEM
@app.delete("/cards/{card_id}", response_model=CardSchema)
def delete_one(card_id: int, db: Session = Depends(get_db)):
    db.query(Cards).filter(Cards.card_id == card_id).delete()
    if card_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Card ID: {card_id} not found!")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
