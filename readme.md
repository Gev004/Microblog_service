# Microblogging FastAPI Project

## 📦 Project Structure
```
Microblog_service/
├── app.py
├── Database/
│   ├── models.py
│   ├── schemas.py
│   └── database.py
├── tests/
│   └── test_main.py
├── Layout/                 # Frontend files
├── nginx/
│   └── default.conf        # Nginx config
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
HOST=IP_ADDRESS_OF_PC_WHERE_DB_LOCATED
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


