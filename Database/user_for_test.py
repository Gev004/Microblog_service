from sqlalchemy.orm import Session
from Database.database import SessionLocal
from Database.models import User, Tweet
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_key(api_key: str) -> str:
    return pwd_context.hash(api_key)

def verify_key(plain_key: str, hashed_key: str) -> bool:
    return pwd_context.verify(plain_key, hashed_key)


def made_test_user():
    db: Session = SessionLocal()
    raw_api_key = "test"
    hashed_api_key = hash_key(raw_api_key)

    test_user = User(username="gev", api_key=hashed_api_key)

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    tweet1 = Tweet(content="Hello, world!", user_id=test_user.id)
    tweet2 = Tweet(content="Another tweet from test_user", user_id=test_user.id)

    db.add_all([tweet1, tweet2])
    db.commit()

    print(f"Test user created: username={test_user.username}, api_key=HIDDEN")