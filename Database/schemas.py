from typing import List, Optional
from pydantic import BaseModel


class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = []

class TweetResponse(BaseModel):
    result: bool
    tweet_id: int

class MediaResponse(BaseModel):
    result: bool
    media_id: int

class BaseResultResponse(BaseModel):
    result: bool

class FollowResponse(BaseModel):
    result: bool
    message: str

class UnfollowResponse(BaseModel):
    result: bool
    message: str

class LikeUser(BaseModel):
    user_id: int
    name: str

class Author(BaseModel):
    id: int
    name: str

class TweetTimelineItem(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: Author
    likes: List[LikeUser]

class TimelineResponse(BaseModel):
    result: bool
    tweets: List[TweetTimelineItem]
