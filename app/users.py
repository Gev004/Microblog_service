from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from Database.models import User, Follow
from Database.schemas import UserProfileResponse
from Database.database import get_db
from .utils import api_key_checking

router = APIRouter()

@router.get("/api/users/me", response_model=UserProfileResponse)
def get_my_profile(
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db)
):
    user = api_key_checking(db, api_key)

    try:
        followers = (
            db.query(User)
            .join(Follow, Follow.follower_id == User.id)
            .filter(Follow.following_id == user.id)
            .all()
        )
        followers_list = [{"id": follower.id, "name": follower.username} for follower in followers]

        following = (
            db.query(User)
            .join(Follow, Follow.following_id == User.id)
            .filter(Follow.follower_id == user.id)
            .all()
        )
        following_list = [{"id": follow.id, "name": follow.username} for follow in following]

        return {
            "result": True,
            "user": {
                "id": user.id,
                "name": user.username,
                "followers": followers_list,
                "following": following_list,
            },
        }

    except Exception as e:
        return {
            "result": False,
            "error_type": "InternalError",
            "error_message": str(e),
        }

@router.get("/api/users/{user_id}", response_model=UserProfileResponse)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {
            "result": False,
            "error_type": "UserNotFound",
            "error_message": f"User with id {user_id} not found",
        }

    try:
        followers = (
            db.query(User)
            .join(Follow, Follow.follower_id == User.id)
            .filter(Follow.following_id == user.id)
            .all()
        )
        followers_list = [{"id": follower.id, "name": follower.username} for follower in followers]

        following = (
            db.query(User)
            .join(Follow, Follow.following_id == User.id)
            .filter(Follow.follower_id == user.id)
            .all()
        )
        following_list = [{"id": follow.id, "name": follow.username} for follow in following]

        return {
            "result": True,
            "user": {
                "id": user.id,
                "name": user.username,
                "followers": followers_list,
                "following": following_list,
            },
        }

    except Exception as e:
        return {
            "result": False,
            "error_type": "InternalError",
            "error_message": str(e),
        }
