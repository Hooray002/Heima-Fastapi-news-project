from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class NewsItemBase(BaseModel):
    """
    新闻基础模型
    """

    id: int = Field(description="新闻ID")

    title: str = Field(description="新闻标题")
    description: str = Field(description="新闻描述")
    image: str = Field(description="新闻图片")
    author: str = Field(description="新闻作者")
    publish_time: datetime = Field(description="新闻发布时间时间")
    category_id: int = Field(description="新闻分类ID")
    views: int = Field(description="新闻浏览量")

    model_config = ConfigDict(from_attributes=True)

class FavoriteRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class FavoriteNewsItemResponse(NewsItemBase):
    """
    收藏新闻响应模型
    """

    favorite_time: datetime = Field(description="收藏时间")


class FavoriteNewsListResponse(BaseModel):
    """
    收藏记录响应模型
    """

    list: list[FavoriteNewsItemResponse]
    total: int = Field(description="收藏总数总数")
    has_more: bool = Field(alias="hasMore", description="是否有更多数据")

    model_config = ConfigDict(populate_by_name=True)