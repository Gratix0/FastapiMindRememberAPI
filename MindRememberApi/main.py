from fastapi import FastAPI
from users.router import router as users_router

app = FastAPI(
    title="MindRemember API"
)

app.include_router(users_router)