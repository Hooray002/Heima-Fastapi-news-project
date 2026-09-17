from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, Integer, String, Text

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Category(Base):
    __tablename__ = 'news_category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='新闻分类id')
    name: Mapped[str] = mapped_column(String(50), comment='新闻分类名称')
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, comment='新闻分类排序')

class News(Base):
    __tablename__ = 'news'

    __table_args__ = (
        Index('idx_category_id', 'category_id'),  # 为 category_id 创建索引
        Index('idx_publish_time', 'publish_time'),  # 为 publish_time 创建索引
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='新闻id')
    title: Mapped[Optional[str]] = mapped_column(String(100), comment='新闻标题')
    description: Mapped[str] = mapped_column(String(200), comment='新闻简介')
    content: Mapped[str] = mapped_column(Text, comment='新闻内容')
    image: Mapped[Optional[str]] = mapped_column(String(200), comment='新闻图片URL')
    author: Mapped[Optional[str]] = mapped_column(String(50), comment='新闻作者')
    category_id: Mapped[int] = mapped_column(Integer, comment='新闻分类id')
    views: Mapped[int] = mapped_column(Integer, default=0, comment='新闻浏览量')
    publish_time: Mapped[datetime] = mapped_column(DateTime, comment='新闻发布时间')
