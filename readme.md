# Microblog Service 🐦

A lightweight Twitter-like microblogging API built with FastAPI.  
This service allows users to post tweets, upload media, follow/unfollow users, like/unlike tweets, and manage their profiles.

---

## 🚀 Features

- Create and delete tweets
- Upload and attach media to tweets
- Like and unlike tweets
- Follow and unfollow users
- View personal and public user profiles
- Get a timeline of followed users' tweets

---

## 📦 Project Structure

Microblog_service/
├── Database/              # SQLAlchemy models and DB setup
├── app.py                 # Main FastAPI application
├── requirements.txt       # Project dependencies
├── Dockerfile             # Docker image config
├── docker-compose.yml     # Services: FastAPI + Postgres
├── .env                   # Environment variables
├── tests/                 # Unit tests with pytest
└── README.md              # Project documentation
