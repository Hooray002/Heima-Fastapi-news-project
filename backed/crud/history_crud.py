from datetime import datetime

from sqlalchemy import delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.news_model import News
from models.history_model import History
from models.users_model import User

async def is_history(
    news_id: int,
    user: User,
    session: AsyncSession,
):
    stmt = select(History).where(History.news_id == news_id, History.user_id == user.id).limit(1)
    result = await session.execute(stmt)
    history = result.scalars().first()
    return history is not None

async def add_history(
    news_id: int,
    user: User,
    session: AsyncSession,
):
    existing = await is_history(news_id, user, session)
    if existing:
        stmt = (
            update(History)
            .where(History.news_id == news_id, History.user_id == user.id)
            .values(view_time=datetime.now())
        )
        await session.execute(stmt)
        await session.commit()
        result = await session.execute(
            select(History)
            .where(History.news_id == news_id, History.user_id == user.id)
            .order_by(History.view_time.desc())
            .limit(1)
        )
        return result.scalars().first()
    history = History(news_id=news_id, user_id=user.id, view_time=datetime.now())
    session.add(history)
    await session.commit()
    await session.refresh(history)
    return history

async def get_history_count(
    user_id: int,
    session: AsyncSession,
):
    stmt = select(func.count(History.id)).where(History.user_id == user_id)
    result = await session.execute(stmt)
    total = result.scalar() or 0
    return total

async def get_history_list(
    user_id: int,
    offset: int,
    limit: int,
    session: AsyncSession,
):
    stmt = (
        select(News, History.view_time.label("view_time"))
        .join(History, News.id == History.news_id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.all()

async def remove_history(
    news_id: int,
    user: User,
    session: AsyncSession,
):
    stmt = delete(History).where(
        (History.news_id == news_id) | (History.id == news_id),
        History.user_id == user.id
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount

async def clear_history(
    user_id: int,
    session: AsyncSession,
):
    stmt = delete(History).where(History.user_id == user_id)
    result = await session.execute(stmt)
    count = result.rowcount or 0
    await session.commit()
    return count
