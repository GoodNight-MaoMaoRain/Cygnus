from typing import List

from fastapi import APIRouter, UploadFile, Depends, Body
from sqlalchemy.orm import Session

from app.api.super_engineer.dockerfile import DockerfileAPI
from app.db.pg_con import get_db
from app.schemas.schemas_super_engineer import AlgorithmThresholds, VersionModel, VersionInfoModel, \
    UpdateLanguageRequest, ResponseModel, UploadResponse, StretchingThresholds
from app.crud.crud_i18n import CRUDI18N
from app.crud.crud_version_info import CRUDVersion
from app.crud.crud_threshold import CRUDAlgorithmThresholds, CRUDStretchingThresholds
# from app.api.super_engineer.dockerfile import DockerfileAPI
from app.api.super_engineer.i18n import I18NAPI
from app.api.super_engineer.thresholds import AlgorithmThresholdsAPI, StretchingThresholdsAPI
from app.api.super_engineer.version import VersionAPI

router = APIRouter()


@router.get("/project_language", summary='获取当前语言和版本', response_model=ResponseModel)
async def get_info(db: Session = Depends(get_db)):
    crud_i18n = CRUDI18N(db)
    crud_version = CRUDVersion(db)
    i18n_api = I18NAPI(crud_i18n, crud_version)

    response = i18n_api.get_current_language()
    return response


@router.put("/language", summary='设置当前语言', response_model=ResponseModel)
async def set_language(language_request: UpdateLanguageRequest, db: Session = Depends(get_db)):
    crud_i18n = CRUDI18N(db)
    crud_version = CRUDVersion(db)  # 初始化 CRUDVersion
    i18n_api = I18NAPI(crud_i18n, crud_version)  # 传递两个参数
    response = i18n_api.set_language(language_request)
    return response


@router.put("/project_info", summary="修改当前版本", response_model=ResponseModel)
async def set_current_version(version_model: VersionModel, db: Session = Depends(get_db)):
    crud_version = CRUDVersion(db)
    version_api = VersionAPI(crud_version)
    response = version_api.set_current_version(version_model)
    return response


@router.get("/version_info", summary='查看当前版本的版本信息', response_model=ResponseModel)
async def get_current_version_info(db: Session = Depends(get_db)):
    crud_version = CRUDVersion(db)
    version_api = VersionAPI(crud_version)
    response = version_api.get_current_version_info()
    return response


@router.put("/version_info", summary='修改当前版本的信息', response_model=ResponseModel)
async def set_current_version_info(new_info: VersionInfoModel, db: Session = Depends(get_db)):
    crud_version = CRUDVersion(db)
    version_api = VersionAPI(crud_version)
    response = version_api.set_current_version_info(new_info)
    return response


@router.get("/algorithm_thresholds", summary='算法阈值查看接口', response_model=ResponseModel)
async def get_thresholds(db: Session = Depends(get_db)):
    crud_thresholds = CRUDAlgorithmThresholds(db)
    threshold_api = AlgorithmThresholdsAPI(crud_thresholds)
    response = threshold_api.get_thresholds()
    return response


@router.put("/algorithm_thresholds", summary='算法阈值修改接口', response_model=ResponseModel)
async def set_thresholds(new_thresholds: AlgorithmThresholds = Body(...), db: Session = Depends(get_db)):
    crud_thresholds = CRUDAlgorithmThresholds(db)
    threshold_api = AlgorithmThresholdsAPI(crud_thresholds)
    response = threshold_api.set_thresholds(new_thresholds)
    return response


@router.get("/stretching_thresholds", summary="不舒展阈值查看接口", response_model=ResponseModel)
async def get_stretching_thresholds(db: Session = Depends(get_db)):
    crud_stretching_thresholds = CRUDStretchingThresholds(db)
    response = StretchingThresholdsAPI(crud_stretching_thresholds).get_stretching_thresholds()
    return response


@router.put("/stretching_thresholds", summary="不舒展阈值修改接口", response_model=ResponseModel)
async def set_stretching_thresholds(new_stretching_thresholds: StretchingThresholds = Body(...),
                                    db: Session = Depends(get_db)):
    crud_stretching_thresholds = CRUDStretchingThresholds(db)
    response = StretchingThresholdsAPI(crud_stretching_thresholds).set_stretching_thresholds(new_stretching_thresholds)
    return response





@router.post("/upload_dockerfile", summary='Docker文件上传接口', response_model=UploadResponse)
async def upload_dockerfile(files: List[UploadFile]):
    dockerfile_api = DockerfileAPI()
    response = await dockerfile_api.upload_dockerfile(files)
    return response
