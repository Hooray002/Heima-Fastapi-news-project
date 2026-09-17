from fastapi import FastAPI, Depends
from routers import news_router, users_router
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

origins = [
    "http://localhost:6008"
    ]

app = FastAPI()

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router.router)
app.include_router(users_router.router)