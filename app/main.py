from fastapi import FastAPI, Depends
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from .models import Base
from .database import engine
from .routers.card_list_router import card_router
from .routers.current_deck import deck_router

# FASTAPI
app = FastAPI(
    title="Exploding Kittens",
    description="A card game."
)

# ROUTER
app.include_router(card_router, tags=["cards"],
                   responses={418: {"description": "Link Broken"}},
                   )
app.include_router(deck_router, tags=["deck"],
                   responses={418: {"description": "Link Broken"}},
                   )

# EXECUTE TABLE
Base.metadata.create_all(bind=engine)
metadata = MetaData()
session = Session(engine)


# HOME PAGE
@app.get("/")
def root():
    return {"message": "Welcome to Exploding Kitten!"}
