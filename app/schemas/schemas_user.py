from typing import Union

from pydantic import BaseModel, Field

from app.schemas.schemas_base import BaseResponseItem


# 登录接口返回的嵌套用户数据
class LoginUserResponseItem(BaseModel):
    role: str
    user_name: str
    token: str


# 登录接口返回数据
class LoginResponseItem(BaseResponseItem):
    data: Union[LoginUserResponseItem | None] = Field(default={})


# 登录接口请求数据
class LoginRequestItem(BaseModel):
    user_name: str
    password_hash: str

class LoginRequest(BaseModel):
    user_name: str
    password_hash: str


class CreateUserRequest(BaseModel):
    user_name: str
    password: str