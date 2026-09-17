from config.db import get_database
from crud import users_crud
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi import Depends, Header, HTTPException

async def get_current_user(
    db: AsyncSession = Depends(get_database),
    authorization: str = Header(alias="Authorization"),
):
    """获取当前用户"""
    token = authorization.removeprefix("Bearer ")
    user = await users_crud.getUserByToken(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    return user
