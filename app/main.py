from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from Database import create_all, made_test_user
from .tweets import router as tweet_router
from .users import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
        create_all()
        made_test_user()
        yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(tweet_router)

if __name__ == "__main__":
    uvicorn.run(app)
