from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from config import db
from models import news_model
from crud import news_crud

#创建API_Router实例，设置路由前缀和标签
router = APIRouter(prefix="/api/news",tags=["news"])


@router.get("/catogories")
async def get_news_categories(skip: int = 0, limit: int = 100, db: db.AsyncSession = Depends(db.get_database)):
    categories = await news_crud.get_categories(skip=skip, limit=limit, database=db)
    return {
    "code": 200,
    "message": "success",
    "data": categories
    }

@router.get("/list")
async def get_news_list(
    category_id: int = Query(..., alias="catogoryId", description="新闻分类ID"),
    page: int = 1,
    page_size: int = Query(10, alias="pageSize", le=100, description="每页新闻数量"),
    db: db.AsyncSession = Depends(db.get_database)
    ):
    skip = (page - 1) * page_size
    news_list = await news_crud.get_news_list(skip=skip, limit=page_size, database=db)
    total = await news_crud.get_news_count(category_id=category_id, database=db)

    more = False
    if (skip+len(news_list)) < total:
        more = True

    return {
    "code": 200,
    "message": "success",
    "data": {
        "list" : news_list,
        "total": total,
        "hasMore": more
        }
    }

@router.get("/detail")
async def get_news_detail(
    news_id: int = Query(..., alias="id", description="新闻ID"),
    db: db.AsyncSession = Depends(db.get_database)
    ):
    news_detail = await news_crud.get_news_detail(news_id=news_id, database=db)
    relate_news = await news_crud.get_news_relate(news_id=news_id,category = news_detail.category_id, database=db)
    news_views = await news_crud.add_views(news_id=news_id, database=db)
    if news_detail is None:
        return {
            "code": 404,
            "message": "新闻未找到",
            "data": None
        }
    
    return {
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": relate_news
        }
    }