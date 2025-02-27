from fastapi import FastAPI, Depends
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from .models import Base
from .database import engine
from .routers import card_router

# FASTAPI
app = FastAPI(
    title="Exploding Kittens",
    description="A card game."
)

# ROUTER
app.include_router(card_router, tags=["cards"],
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
