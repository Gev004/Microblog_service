from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from Database.models import User

def api_key_checking(db: Session, api_key: str):
    users = db.query(User).all()
    for user in users:
        if bcrypt.verify(api_key, user.api_key):
            return user
    raise HTTPException(status_code=401, detail="Invalid API Key")
