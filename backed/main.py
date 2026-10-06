from fastapi import FastAPI, Depends
from routers import history_routers
from routers import favorite_router
from routers import news_router, users_router
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:6008",
    "http://127.0.0.1:6008",
]

app = FastAPI()

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router.router)
app.include_router(users_router.router)
app.include_router(favorite_router.router)
app.include_router(history_routers.router)