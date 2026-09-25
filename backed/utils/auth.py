from typing import Optional

from config.db import get_database
from crud import users_crud
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi import Depends, Header, HTTPException

async def get_current_user(
    db: AsyncSession = Depends(get_database),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
):
    """获取当前用户"""
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    user = await users_crud.getUserByToken(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")
    return user
