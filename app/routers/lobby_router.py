from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import LobbyModel
from ..database import get_db
from ..schema import Lobby

lobby_router = APIRouter(
    prefix="/lobby",
    tags=["lobby"])
