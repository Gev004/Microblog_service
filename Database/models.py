from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from Database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    tweets = relationship("Tweet", back_populates="user")


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="tweets")
    media = relationship("Media", back_populates="tweet")


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    file_path = Column(String, nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), nullable=True)

    tweet = relationship("Tweet", back_populates="media")


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), nullable=False)

    user = relationship("User", backref="likes")
    tweet = relationship("Tweet", backref="likes")

    __table_args__ = (UniqueConstraint('user_id', 'tweet_id', name='_user_tweet_uc'),)

class Follow(Base):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    following_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='unique_follow'),
    )

    follower = relationship("User", foreign_keys=[follower_id], backref="following")
    following = relationship("User", foreign_keys=[following_id], backref="followers")