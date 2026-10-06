from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class HistoryItemBase(BaseModel):
    """
    历史浏览记录基础模型
    """

    id: int = Field(description="新闻ID")

    title: Optional[str] = Field(None, description="新闻标题")
    description: Optional[str] = Field(None, description="新闻描述")
    image: Optional[str] = Field(None, description="新闻图片")
    author: Optional[str] = Field(None, description="新闻作者")
    publish_time: Optional[datetime] = Field(None, description="新闻发布时间", serialization_alias="publishTime")
    category_id: Optional[int] = Field(None, description="新闻分类ID", serialization_alias="categoryId")
    views: int = Field(0, description="新闻浏览量")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class HistoryRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HistoryResponse(BaseModel):
    """
    添加历史浏览记录响应模型
    """
    id: int = Field(description="历史记录ID")
    user_id: int = Field(description="用户ID", serialization_alias="userId")
    news_id: int = Field(description="新闻ID", serialization_alias="newsId")
    view_time: Optional[datetime] = Field(None, description="浏览时间", serialization_alias="viewTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class HistoryNewsItemResponse(HistoryItemBase):
    """
    历史浏览新闻项响应模型（包含浏览时间）
    """

    view_time: Optional[datetime] = Field(None, description="浏览时间", serialization_alias="viewTime")


class HistoryNewsListResponse(BaseModel):
    """
    历史浏览记录响应模型
    """

    list: list[HistoryNewsItemResponse]
    total: int = Field(description="历史浏览记录总数")
    has_more: bool = Field(alias="hasMore", description="是否有更多数据")

    model_config = ConfigDict(populate_by_name=True)