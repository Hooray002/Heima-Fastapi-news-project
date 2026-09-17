from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from config import db
from models import users_model
from crud import users_crud
from schemas import users_schemas
from utils.response import success_response
from schemas.users_schemas import UserAuthResponse, UserInfoResponse
from utils import auth

router = APIRouter(prefix = "/api/user", tags = ["users"])

@router.post("/register")
async def register(user_data: users_schemas.users_request, db: db.AsyncSession = Depends(db.get_database)):
    user_name = await users_crud.get_user_name(user_data.username, db)
    if user_name is not None:
        raise HTTPException(status_code=400, detail="用户已存在")
    user = await users_crud.user_register(user_data=user_data, database=db)
    token = await users_crud.create_token(user_id=user.id, database=db)
    user_response = UserAuthResponse(token=token, user_info = UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=user_response)

@router.post("/login")
async def login(user_data: users_schemas.users_request, db: db.AsyncSession = Depends(db.get_database)):
    user = await users_crud.user_login(user_data=user_data, database=db)
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    token = await users_crud.create_token(user_id=user.id, database=db)
    user_response = UserAuthResponse(token=token, user_info = UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=user_response)

@router.get("/info")
async def info(user: users_model.User = Depends(auth.get_current_user)):
    """获取用户信息"""
    return success_response(
        message="success", data=UserInfoResponse.model_validate(user)
    )