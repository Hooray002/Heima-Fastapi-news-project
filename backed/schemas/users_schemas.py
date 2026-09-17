from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class users_request(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    username: str
    password: str

class UserInfoResponse(UserInfoBase):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=521, description="简介")

    model_config = ConfigDict(
        from_attributes=True
    )

class UserAuthResponse(BaseModel):
    token: str
    user_info : UserInfoResponse = Field(...,alias="userInfo")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
