from fastapi import APIRouter, Depends, HTTPException, Path, Query

from crud import history_crud
from utils.response import success_response
from config import db
from models.users_model import User
from utils.auth import get_current_user
from schemas.history_schemas import HistoryNewsListResponse, HistoryNewsItemResponse, HistoryRequest, HistoryResponse

router = APIRouter(prefix="/api/history", tags=["History"])

@router.get("/list")
async def get_history_list(
    page: int=Query(1, description="页码"),
    page_size: int=Query(10, alias="pageSize", description="每页数量"),
    user: User = Depends(get_current_user),
    session: db.AsyncSession = Depends(db.get_database)
):
    offset = (page - 1) * page_size
    total = await history_crud.get_history_count(user.id, session)
    result = await history_crud.get_history_list(user.id, offset, page_size, session)
    history_list = [
        HistoryNewsItemResponse.model_validate(
            {**news.__dict__, "view_time": view_time}
        )
        for news, view_time in result
    ]
    data = HistoryNewsListResponse(list=history_list, total=total, has_more=(offset + len(result) < total))
    return success_response(data=data)

@router.post("/add")
async def add_history(
    data: HistoryRequest,
    user: User = Depends(get_current_user),
    session: db.AsyncSession = Depends(db.get_database)
):
    result = await history_crud.add_history(news_id=data.news_id, user=user, session=session)
    response_data = HistoryResponse.model_validate(result)
    return success_response(message="历史浏览记录添加成功", data=response_data)

@router.delete("/delete/{news_id}")
async def remove_history(
    news_id: int = Path(..., description="新闻ID"),
    user: User = Depends(get_current_user),
    session: db.AsyncSession = Depends(db.get_database)
):
    count = await history_crud.remove_history(news_id=news_id, user=user, session=session)
    if count == 0:
        raise HTTPException(status_code=404, detail="历史浏览记录不存在")
    return success_response(message="历史浏览记录删除成功")

@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),
    session: db.AsyncSession = Depends(db.get_database)
):
    count = await history_crud.clear_history(user_id=user.id, session=session)
    return success_response(message=f"历史浏览记录清空成功,清除了{count}条记录")
