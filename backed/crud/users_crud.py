from datetime import timedelta, datetime
import uuid

from fastapi import Depends
from sqlalchemy import func, update
from config import db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.users_model import User, UserToken
from schemas import users_schemas
from utils.security import get_hash_password, verify_password


async def get_user_name(user_name: str, database: AsyncSession = Depends(db.get_database)):
    result = await database.execute(select(User).where(user_name == User.username))
    result_name = result.scalar_one_or_none()
    return result_name

async def user_register(user_data: users_schemas.users_request, database: AsyncSession = Depends(db.get_database)):
    hash_password = get_hash_password(user_data.password)
    user = User(username = user_data.username, password = hash_password)
    database.add(user)
    await database.commit()
    await database.refresh(user)
    return user

async def create_token(user_id: int, database: AsyncSession=Depends(db.get_database)):
    token = str(uuid.uuid4())
    expires_at = datetime.now()+timedelta(days=7)
    result = await database.execute(select(UserToken).where(UserToken.user_id == user_id))
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
    else:
        user_token = UserToken(user_id = user_id, token = token, expires_at = expires_at)
        database.add(user_token)
    await database.commit()
    return token

async def user_login(user_data: users_schemas.users_request, database: AsyncSession = Depends(db.get_database)):
    user = await get_user_name(user_data.username, database)
    if not user:
        return None
    pw = verify_password(user_data.password, user.password)
    if pw:
        return user
    else:
        return None

async def getUserByToken(db: AsyncSession, token: str):
    """根据token查询用户"""
    # 先查询token是否存在，是否过期
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    userToken = result.scalars().one_or_none()
    if not userToken or userToken.expires_at < datetime.now():
        return None

    # 再根据token查询用户
    stmt = select(User).where(User.id == userToken.user_id)
    result = await db.execute(stmt)
    user = result.scalars().one_or_none()
    return user
