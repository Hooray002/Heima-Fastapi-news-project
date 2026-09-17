from fastapi import Depends
from sqlalchemy import func, update
from config import db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.news_model import Category, News

async def get_categories(skip: int = 0, limit: int = 100, database: AsyncSession = Depends(db.get_database)):
    result = await database.execute(select(Category).offset(skip).limit(limit))
    categories = result.scalars().all()
    return categories

async def get_news_list(skip: int = 0, limit: int = 100, database: AsyncSession = Depends(db.get_database)):
    result = await database.execute(select(News).offset(skip).limit(limit))
    news_list = result.scalars().all()
    return news_list

async def get_news_count(category_id: int, database: AsyncSession = Depends(db.get_database)):
    result = await database.execute(select(func.count(News.id)).where(News.category_id == category_id))
    news_count = result.scalar()
    return news_count

async def get_news_detail(news_id: int, database: AsyncSession = Depends(db.get_database)):
    result = await database.execute(select(News).where(News.id == news_id))
    news_detail = result.scalar_one_or_none()
    return news_detail

async def get_news_relate(news_id: int, category: int, database: AsyncSession = Depends(db.get_database)):
    result = await database.execute(select(News).where((News.id != news_id) & (News.category_id == category)).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(5))
    news_relate = result.scalars().all()
    return news_relate

async def add_views(news_id: int, database: AsyncSession = Depends(db.async_engine)):
    result = update(News).where(news_id == News.id).values(views = News.views + 1)
    await database.execute(result)
    await database.commit()