from sqlalchemy.orm import Session
from Database.database import SessionLocal
from Database.models import User, Tweet

def made_test_user():
    db: Session = SessionLocal()
    api_key = "test"
    test_user = User(username="gev", api_key=api_key)

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    tweet1 = Tweet(content="Hello, world!", user_id=test_user.id)
    tweet2 = Tweet(content="Another tweet from test_user", user_id=test_user.id)

    db.add_all([tweet1, tweet2])
    db.commit()

    print(f"Test user created: username={test_user.username}, api_key={test_user.api_key}")