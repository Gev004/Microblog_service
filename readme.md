# Microblogging FastAPI Project

## 📦 Project Structure
```
Microblog_service/
│
├── app/
│   ├── __init__.py   
│   ├── main.py 
│   ├── tweets.py
│   ├── users.py
│   ├── utils.py      
│
├── Database/
│   ├── __init__.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── user_for_test.py
│
├── tests/
│   ├── conftest.py
│   ├── test_endpoints.py
│
├── Layout/
│   ├── dist/
│       ├──css/
│       ├──js/
│       ├──favicon.ico
│       ├──index.html   
│
├── nginx/
│   └── default.conf
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md

```

## 🚀 Getting Started
### 1. Clone the repository
```bash
git clone https://github.com/gevorg_sargsyan/microblog-service.git
cd microblog-service
```

### 2. Create `.env` file
Create a `.env` file in the root directory with the following content:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=yourdbname
HOST=db
```

### 3. Build and start the containers
```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost
- Swagger UI: http://localhost:8000/docs

### 4. Run Migrations (if using Alembic)
```bash
docker exec -it fastapi_backend alembic upgrade head
```

## 🧪 Run Tests
```bash
docker exec -it fastapi_backend pytest
```

## 📂 API Overview
- `POST /api/tweets` — Create a tweet
- `DELETE /api/tweets/{id}` — Delete tweet
- `POST /api/medias` — Upload media file
- `POST /api/tweets/{id}/likes` — Like tweet
- `DELETE /api/tweets/{id}/likes` — Remove like
- `POST /api/tweets/{user_id}/follow` — Follow user
- `DELETE /api/tweets/{user_id}/unfollow` — Unfollow user
- `GET /api/tweets` — Get timeline
- `GET /api/users/me` — View own profile
- `GET /api/users/{user_id}` — View other profile

All API requests require `api-key` header.


