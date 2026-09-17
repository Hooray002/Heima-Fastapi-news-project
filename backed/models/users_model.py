from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String, Text

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        Index("username_UNIQUE","username"),
        Index("phone_UNIQUE","phone"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default="https://default-avatar.png",
        comment="头像地址"
    )
    gender: Mapped[Optional[str]] = mapped_column(
        Enum("male", "female", "unknown"),
        nullable=True,
        comment="性别 male-男 female-女 unknown-未知"
    )
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="个人简介")
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True, comment="手机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

class UserToken(Base):

    __tablename__ = 'user_token'

    __table_args__ = (
        Index("fk_user_token_user_idx", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="令牌ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")