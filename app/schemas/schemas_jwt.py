from datetime import datetime

from pydantic import BaseModel


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    user_name: str
    user_id: str
