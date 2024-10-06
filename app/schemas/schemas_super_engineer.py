from pydantic import BaseModel
from typing import Union, Optional


class UpdateLanguageRequest(BaseModel):
    language: str


class VersionInfoModel(BaseModel):
    software_python: Optional[str]
    software_ui: Optional[str]
    software_go: Optional[str]
    hardware: Optional[str]
    ALG_white: Optional[str]
    ALG_red: Optional[str]
    ALG_pc: Optional[str]
    release_num: Optional[str]


class VersionModel(BaseModel):
    version_name: str


class ResponseModel(BaseModel):
    errno: str
    errmsg: str
    data: Optional[Union[str, dict]]


class AlgorithmThresholds(BaseModel):
    WhiteSize: float
    RedSize: float
    PCSize: float
    ThinkSize: float
    PlateletSize: float
    MicroSize: float


class StretchingThresholds(BaseModel):
    StretchingSize: float


class UploadResponse(BaseModel):
    errno: str
    errmsg: str
    data: Optional[dict] = None
