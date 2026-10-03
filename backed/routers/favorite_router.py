from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import Field

from schemas.favorite_schemas import FavoriteNewsItemResponse, FavoriteNewsListResponse, FavoriteRequest
from crud.favorite_crud import is_favorite
from models.favorite_model import Favorite
from utils.response import success_response
from config import db
from crud import news_crud, favorite_crud
from models.users_model import User
from utils.auth import get_current_user

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId", description="新闻ID"),
    user: User = Depends(get_current_user),
    db: db.AsyncSession = Depends(db.get_database)
    ):
    favorite = await is_favorite(news_id, user, db)
    return success_response(message="查询收藏新闻状态成功", data = favorite)

@router.post("/add")
async def add_favorite(
    data: FavoriteRequest,
    user: User = Depends(get_current_user),
    db: db.AsyncSession = Depends(db.get_database)
    ):
    favorite = await is_favorite(data.news_id, user, db)
    if not favorite:
        favorite_result = await favorite_crud.add_favorite(data.news_id, user, db)
        return success_response(message="收藏新闻成功", data = favorite_result)
    return success_response(message="新闻已收藏")

@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId", description="新闻ID"),
    user: User = Depends(get_current_user),
    db: db.AsyncSession = Depends(db.get_database)
    ):
    favorite = await is_favorite(news_id, user, db)
    if not favorite:
        raise HTTPException(status_code=404, detail="新闻未收藏")
    result = await favorite_crud.remove_favorite(news_id, user, db)
    return success_response(message="取消收藏新闻成功")

@router.get("/list")
async def get_favorite_list(
    page: int=Query(1, description="页码"),
    page_size: int=Query(10, alias="pageSize", description="每页数量"),
    user: User = Depends(get_current_user),
    db: db.AsyncSession = Depends(db.get_database)
):
    offset = (page - 1) * page_size
    total = await favorite_crud.get_favorite_count(user.id, db)
    result = await favorite_crud.get_favorite_list(user.id, offset, page_size,db)
    favorite_list = [
        FavoriteNewsItemResponse.model_validate(
            {**news.__dict__, "favorite_time": favorite_time}
        )
        for news, favorite_time in result
    ]
    data = FavoriteNewsListResponse(
        list=favorite_list, total=total, has_more=(offset + len(result) < total)
    )
    return success_response(data=data)

@router.delete("/clear")
async def clear_favorite(
    user: User = Depends(get_current_user),
    db: db.AsyncSession = Depends(db.get_database)
):
    result = await favorite_crud.clear_favorite(user.id, db)
    return success_response(message=f"清空收藏新闻成功,清除了{result}条记录")