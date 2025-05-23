import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from Database.database import Base, get_db
from Database.models import User
from app import app
from Database.user_for_test import hash_key

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="function")
def test_user(db):
    raw_api_key = uuid4().hex
    hashed_api_key = hash_key(raw_api_key)

    user = User(username=f"user_{uuid4().hex}", api_key=hashed_api_key)
    db.add(user)
    db.commit()
    db.refresh(user)

    user.raw_api_key = raw_api_key
    return user
