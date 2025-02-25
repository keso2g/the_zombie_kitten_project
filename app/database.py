from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ENGINE
postgres_url = URL.create(
    "postgresql",
    username=os.environ.get("USERNAME"),
    password=os.environ.get("PASSWORD"),
    host=os.environ.get("HOST"),
    database=os.environ.get("DATABASE")
)

engine = create_engine(postgres_url)


# SESSION
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
