from typing import Optional

from fastapi import Depends
from sqlalchemy import delete, func, update
from crud import history_crud
from config import db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.news_model import Category, News
from models.favorite_model import Favorite
from models.users_model import User

async def is_favorite(news_id: int, user: User, db: AsyncSession):
    query = select(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user.id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None

async def add_favorite(news_id: int, user: User, db: AsyncSession):
    favorite = Favorite(news_id=news_id, user_id=user.id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_favorite(news_id: int, user: User, db: AsyncSession):
    stmt = delete(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user.id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount

async def get_favorite_list(
    user_id: int,
    offset: int,
    page_size: int,
    db: AsyncSession,
):
    stmt = ( 
    select(
        News, Favorite.created_at.label("favorite_time"))
        .join(Favorite, News.id == Favorite.news_id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
        )
    result = await db.execute(stmt)
    return result.all()

async def get_favorite_count(user_id: int, db: AsyncSession):
    result = await db.execute(select(func.count(Favorite.id)).where(Favorite.user_id == user_id))
    return result.scalar()

async def clear_favorite(user_id: int, db: AsyncSession):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    count = result.rowcount
    await db.commit()
    return count