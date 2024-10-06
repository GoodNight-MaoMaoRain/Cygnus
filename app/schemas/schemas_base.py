from typing import Any

from pydantic import BaseModel


class BaseResponseItem(BaseModel):
    errno: str
    errmsg: str



