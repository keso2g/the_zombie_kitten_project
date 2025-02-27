from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Deck
from ..database import get_db
from ..schema import CurrentDeck

deck_router = APIRouter(
    prefix="/deck",
    tags=["deck"])


# VIEW ALL ITEMS
@deck_router.get("/", response_model=list[CurrentDeck])
def view(db: Session = Depends(get_db)):
    cards = db.query(Deck).order_by(Deck.current_deck_id).all()
    return cards


# VIEW AN ITEM
@deck_router.get("/{id}", response_model=CurrentDeck, tags=["deck"])
def get_one(id: int, db: Session = Depends(get_db)):
    view = db.query(Deck).filter(Deck.current_deck_id == id).first()
    if not view:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Card ID: {id} not found!")
    return view


# GET CARD USING QUERY PARAMS
@deck_router.get("/search_deck_query/", response_model=CurrentDeck, tags=["deck"])
def get_one(q: str, values: int = None, db: Session = Depends(get_db)):
    if q:
        if q == "current_deck_id":
            view = db.query(Deck).filter(
                Deck.current_deck_id == values).first()
            return (view)
        elif q != "current_deck_id":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Please use a valid query!")


# ADD AN ITEM
@deck_router.post("/add_info/", response_model=CurrentDeck, status_code=status.HTTP_201_CREATED, tags=["deck"])
def add_one(card: CurrentDeck, db: Session = Depends(get_db)):
    add_card = Deck(
        current_deck_id=card.current_deck_id,
        lobby_id=card.lobby_id,
        card_array=card.card_array,
        discard_array=card.discard_array,
        zombie_kitten_count=card.zombie_kitten_count,
        exploding_kitten_count=card.exploding_kitten_count
    )

    db.add(add_card)
    db.commit()
    db.refresh(add_card)
    return add_card


# UPDATE A CARD
@deck_router.put("/update_card/{id}", response_model=CurrentDeck, status_code=status.HTTP_202_ACCEPTED, tags=["deck"])
def update_card(id: int, card: CurrentDeck, db: Session = Depends(get_db)):
    id_filter = db.query(Deck).filter(Deck.current_deck_id == id).first()
    if id_filter == None:
        raise HTTPException(
            status_code=404, detail=f"Card ID: {id} not found!")
    id_filter.current_deck_id = card.current_deck_id
    id_filter.lobby_id = card.lobby_id
    id_filter.card_array = card.card_array
    id_filter.discard_array = card.discard_array
    id_filter.zombie_kitten_count = card.zombie_kitten_count
    id_filter.exploding_kitten_count = card.exploding_kitten_count

    db.commit()
    return id_filter


# DELETE AN ITEM
@deck_router.delete("/{id}", response_model=CurrentDeck, tags=["deck"])
def delete_one(id: int, db: Session = Depends(get_db)):
    db.query(Deck).filter(Deck.current_deck_id == id).delete()
    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Card ID: {id} not found!")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
