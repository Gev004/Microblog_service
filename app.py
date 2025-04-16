from typing import Type
from uuid import uuid4
import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Header, HTTPException, UploadFile, File, Path
from sqlalchemy.orm import Session
from Database.models import User, Tweet, Media, Like, Follow
from Database.schemas import *
from Database.database import get_db,create_all


def api_key_checking(db: Session,api_key: str) -> Type[User]:
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return user


@asynccontextmanager
async def lifespan(app: FastAPI):
        create_all()
        yield

app = FastAPI(lifespan=lifespan)

FOLDER_NAME = "static"
os.makedirs(FOLDER_NAME, exist_ok=True)




@app.post("/api/tweets",response_model=TweetResponse)
def create_tweet(
    tweet: TweetCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(..., alias="api-key"),
):

    user = api_key_checking(db,api_key)

    if not tweet.tweet_data.strip():
        raise HTTPException(status_code=400, detail="Tweet data cannot be empty")

    new_tweet = Tweet(content=tweet.tweet_data, user_id=user.id)
    db.add(new_tweet)
    db.flush()

    if tweet.tweet_media_ids:
        media_items = db.query(Media).filter(Media.id.in_(tweet.tweet_media_ids)).all()
        for media in media_items:
            media.tweet_id = new_tweet.id
    db.commit()

    return TweetResponse(result=True, tweet_id=new_tweet.id)

@app.post("/api/medias",response_model=MediaResponse)
def create_media(
    api_key: str = Header(..., alias="api-key"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    user = api_key_checking(db,api_key)

    filename = f"{uuid4().hex}_{file.filename}"
    file_path = os.path.join(FOLDER_NAME, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    media = Media(file_path=file_path)
    db.add(media)
    db.commit()
    db.refresh(media)

    return {"result": True, "media_id": media.id}

@app.delete("/api/tweets/{tweet_id}",response_model=BaseResultResponse)
def delete_tweets(
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db),
    tweet_id: int = Path(...),
):
    user = api_key_checking(db,api_key)

    tweet = db.query(Tweet).filter(Tweet.user_id == user.id,Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found or not yours")
    db.delete(tweet)
    db.commit()

    return {"result": True}


@app.post("/api/tweets/{tweet_id}/likes",response_model=BaseResultResponse)
def likes(
    tweet_id = Path(...),
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db),
):
    user = api_key_checking(db,api_key)

    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    existing_like = db.query(Like).filter_by(user_id=user.id, tweet_id=tweet.id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="You already liked this tweet")

    like = Like(user_id=user.id, tweet_id=tweet.id)
    db.add(like)
    db.commit()

    return {"result": True}

@app.delete("/api/tweets/{tweet_id}/remove_likes",response_model=BaseResultResponse)
def delete_likes(
    tweet_id = Path(...),
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db),
):
    user = api_key_checking(db,api_key)

    tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    existing_like = db.query(Like).filter_by(user_id=user.id, tweet_id=tweet.id).first()
    if not existing_like:
        raise HTTPException(status_code=400, detail="You haven't liked this tweet")

    db.delete(existing_like)
    db.commit()

    return {"result": True}

@app.post("/api/tweets/{user_id}/follow",response_model=FollowResponse)
def follow(
    user_id: int = Path(...),
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db),
):
    follower = api_key_checking(db,api_key)

    if follower.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    following = db.query(User).filter(User.id == user_id).first()
    if not following:
        raise HTTPException(status_code=404, detail="User to follow not found")

    existing_follow = db.query(Follow).filter_by(follower_id=follower.id, following_id=user_id).first()
    if existing_follow:
        raise HTTPException(status_code=400, detail="You already follow this user")

    follow = Follow(follower_id=follower.id, following_id=user_id)
    db.add(follow)
    db.commit()

    return {"result": True, "message": f"You are now following {following.username}"}

@app.delete("/api/tweets/{user_id}/unfollow",response_model=UnfollowResponse)
def unfollow(
    user_id: int = Path(...),
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db),
):
    follower = api_key_checking(db,api_key)

    if follower.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    following = db.query(User).filter(User.id == user_id).first()
    if not following:
        raise HTTPException(status_code=404, detail="User to follow not found")

    existing_follow = db.query(Follow).filter_by(follower_id=follower.id, following_id=user_id).first()
    if not existing_follow:
        raise HTTPException(status_code=400, detail="You are not following this user")


    db.delete(existing_follow)
    db.commit()

    return {"result": True, "message": f"You have unfollowed {following.username}"}


@app.get("/api/tweets", response_model=TweetResponse)
def get_timeline(
        api_key: str = Header(..., alias="api-key"),
        db: Session = Depends(get_db),
):
    user = api_key_checking(db, api_key)

    try:
        following_ids = db.query(Follow.following_id).filter(Follow.follower_id == user.id).all()
        following_ids = [f.following_id for f in following_ids]

        tweets = db.query(Tweet).filter(Tweet.user_id.in_(following_ids)).order_by(Tweet.created_at.desc()).all()

        result_tweets = []
        for tweet in tweets:
            media_links = db.query(Media).filter(Media.tweet_id == tweet.id).all()
            media_links = [media.file_path for media in media_links]

            likes = db.query(Like).filter(Like.tweet_id == tweet.id).all()
            like_users = [
                {"user_id": like.user_id, "name": db.query(User).filter(User.id == like.user_id).first().username}
                for like in likes
            ]

            result_tweets.append({
                "id": tweet.id,
                "content": tweet.content,
                "attachments": media_links,
                "author": {"id": tweet.user_id,
                           "name": db.query(User).filter(User.id == tweet.user_id).first().username},
                "likes": like_users
            })

        return {"result": True, "tweets": result_tweets}

    except Exception as e:
        return {"result": False, "error_type": "InternalError", "error_message": str(e)}

@app.get("/api/users/me",response_model=TweetTimelineItem)
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


@app.get("/api/users/{user_id}",response_model=TimelineResponse)
def get_user_profile(
    user_id: int = Path(...),
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


if __name__ == "__main__":
    uvicorn.run(app)