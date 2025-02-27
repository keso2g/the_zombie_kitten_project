from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import Cards
from .database import get_db
from .schema import CardSchema

card_router = APIRouter(
    prefix="/cards",
    tags=["cards"])
#     dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )


# VIEW ALL ITEMS
@card_router.get("/", response_model=list[CardSchema])
def view(db: Session = Depends(get_db)):
    cards = db.query(Cards).order_by(Cards.card_id).all()
    return cards


# ADD AN ITEM
@card_router.post("/add_card/", response_model=CardSchema, status_code=status.HTTP_201_CREATED, tags=["cards"])
def add_one(card: CardSchema, db: Session = Depends(get_db)):
    add_card = Cards(
        card_name=card.card_name,
        card_description=card.card_description,
        is_exploding_kitten=card.is_exploding_kitten,
        is_zombie_kitten=card.is_zombie_kitten,
        card_type=card.card_type,
        img_path=card.img_path,
        is_now=card.is_now,
        with_cat_paw=card.with_cat_paw,
        card_count=card.card_count
    )

    db.add(add_card)
    db.commit()
    db.refresh(add_card)
    return add_card


# UPDATE A CARD
@card_router.put("/update_card/{id}", response_model=CardSchema, status_code=status.HTTP_202_ACCEPTED, tags=["cards"])
def update_card(id: int, card: CardSchema, db: Session = Depends(get_db)):
    id_filter = db.query(Cards).filter(Cards.card_id == id).first()
    if id_filter == None:
        raise HTTPException(
            status_code=404, detail=f"Card ID: {id} not found!")
    id_filter.card_name = card.card_name
    id_filter.card_description = card.card_description
    id_filter.is_exploding_kitten = card.is_exploding_kitten
    id_filter.is_zombie_kitten = card.is_zombie_kitten
    id_filter.card_type = card.card_type
    id_filter.img_path = card.img_path
    id_filter.is_now = card.is_now
    id_filter.with_cat_paw = card.with_cat_paw
    id_filter.card_count = card.card_count

    db.commit()
    return id_filter


# VIEW AN ITEM
@card_router.get("/{id}", response_model=CardSchema, tags=["cards"])
def get_one(id: int, db: Session = Depends(get_db)):
    view = db.query(Cards).filter(Cards.card_id == id).first()
    if not view:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Card ID: {id} not found!")
    return view


# GET CARD USING QUERY PARAMS
@card_router.get("/search_query/", response_model=CardSchema, tags=["cards"])
def get_one(q: str, values: int = None, db: Session = Depends(get_db)):
    if q:
        if q == "card_id":
            view = db.query(Cards).filter(Cards.card_id == values).first()
            return (view)
        elif q != "card_id":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Please use a valid query!")


# DELETE AN ITEM
@card_router.delete("/{card_id}", response_model=CardSchema, tags=["cards"])
def delete_one(card_id: int, db: Session = Depends(get_db)):
    db.query(Cards).filter(Cards.card_id == card_id).delete()
    if card_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Card ID: {card_id} not found!")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
