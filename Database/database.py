import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

password = os.getenv("POSTGRES_PASSWORD")
username = os.getenv("POSTGRES_USER")
database = os.getenv("POSTGRES_DB")
host = os.getenv("HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}:5432/{database}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_all():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

