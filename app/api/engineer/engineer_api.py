from fastapi import APIRouter, Depends, Query, Body, HTTPException, Request
from sqlalchemy.orm import Session
from app.api.auth2.jwt import verify_access_token, get_current_user
from app.api.engineer.dynamic_routing import get_routes_based_on_role
# from app.api.engineer.dynamic_routing import dynamic_router
from app.api.engineer.reboot_service import RebootService
from app.api.engineer.test import TestServer
from app.core.settings.base import RestartType
from app.db.pg_con import get_db
from app.api.engineer.camerapicture_controller import CameraPictureController
from app.api.engineer.data_back import DataBack
from app.api.engineer.finalversion_controller import FinalVersionController
from app.api.engineer.hardware_controller import HardwareController
from app.api.engineer.logs_controller import LogsController
from app.api.engineer.setmarkhide_controller import SetMarkHideController
from app.api.engineer.sysstatus_controller import SysStatusController
from app.schemas.schemas_engineer import *
from app.orm.models import SimulationData

router = APIRouter()


# ############################## LogsController ##############################
@router.get('/logs/files', response_model=LogModules, summary='列出日志文件')
async def list_log_files():
    return LogsController.get_instance().list_log_files()


@router.post('/download_logs', summary='日志下载')
async def download_logs(request: LogRequest = Body(..., description='可传参数为 python Go product hardware')):
    return LogsController.get_instance().download_logs(request.log_type)


@router.post("/logs", response_model=LogResponse, summary="日志筛选")
async def logs(params: LogFilterParams):
    return LogsController.get_instance().logs(params)


@router.post("/backups", response_model=BackResponse, summary='备份')
async def get_back(request: BackupRequest, db: Session = Depends(get_db)):
    return TestServer.get_back(request, db)


@router.post("/export", response_model=ExportResponse, summary="导出数据")
async def export_data(request: ExportRequest):
    return TestServer.export_data(request)


@router.post("/search", response_model=SearchResponse, summary="数据搜索")
async def search_data(request: SearchRequest, db: Session = Depends(get_db)):
    return await TestServer.search_data(request, db)


# ############################## SysStatusController ##############################
@router.get("/sys_status", response_model=SystemStatusResponseModel, summary='获取系统完整状态')
async def sys_status():
    status = SysStatusController.get_instance().get_sys_status()
    return SystemStatusResponseModel(**status)


@router.get("/running_status", response_model=HardwareStatusResponseModel, summary='获取硬件运行状态')
async def running_status():
    status = SysStatusController.get_instance().running_status()
    return status


@router.get("/sensor_status", response_model=SensorStatusResponseModel, summary='获取传感器状态')
async def sensor_status():
    status = SysStatusController.get_instance().sensor_status()
    return status


@router.get("/top_command", response_model=CommandOutputResponseModel, summary='返回系统进程信息')
async def top_command():
    data = SysStatusController.get_instance().top_command()
    return data


@router.get("/nvidia_command", response_model=CommandOutputResponseModel, summary='返回GPU状态')
async def nvidia_command():
    data = SysStatusController.get_instance().nvidia_command()
    return data


@router.get("/python_server", response_model=PythonServerResponseModel, summary='获取Python服务器状态')
async def python_server():
    status = SysStatusController.get_instance().python_server()
    return status


@router.get("/go_server", response_model=GoServerResponseModel, summary='获取Go服务器状态')
async def go_server(db: Session = Depends(get_db)):
    status = SysStatusController.get_instance().go_server(db)
    return status


@router.get("/system_status", response_model=SysStatusResponseModel, summary='获取系统整状态')
async def system_status():
    status = SysStatusController.get_instance().get_system_status()
    return SysStatusResponseModel(**status)


# ############################## DataBack ##############################
@router.get('/sql_back_data', response_model=BackupResponse, summary='导出数据库数据')
async def sql_back_data():
    return DataBack.get_instance().sql_back_data()


@router.post('/task_back_data', response_model=BackupResponse, summary='导出任务数据并保存到数据库')
async def task_back_data(task_ids: str):
    return DataBack.get_instance().task_back_data(task_ids)


# ############################## HardwareController ##############################
@router.get('/running_hardware_status', response_model=HardwareControllerResponse, summary='获取硬件状态信息')
async def running_hardware_status(db: Session = Depends(get_db)):
    return HardwareController.get_instance().running_hardware_status(db)


# ############################## CameraPictureController ##############################
@router.get('/qrcamera_picture', response_model=CameraPictureResponse, summary=" 获取下位机二维码相机拍照图片")
async def get_QRcamera_picture():
    return CameraPictureController.get_instance().get_QRcamera_picture()


# ############################## FinalVersionController ##############################
@router.get('/final_version', response_model=FinalVersionControllerResponse, summary="读取并返回部署版本信息")
async def final_version(session: Session = Depends(get_db)):
    return FinalVersionController.get_instance().final_version(session)


# ############################## SetMarkHideController ##############################
@router.get('/set_mark_hide', response_model=SetMarkHideControllerResponse, summary="更新标记数据")
async def set_mark_hide(mark_file: Optional[bool] = Query(False), mark_data: Optional[bool] = Query(False),
                        mark_id: int = 1, db: Session = Depends(get_db)):
    return SetMarkHideController.get_instance().set_mark_hide(db, mark_file, mark_data, mark_id)


# ###############################        add api           ############################
@router.get("/get_async_routes", summary='获取动态路由')
async def get_async_routes(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_role = int(current_user.get("role"))
    return get_routes_based_on_role(user_role, db)


@router.get('/get_hide')
def get_hide(db: Session = Depends(get_db)):
    return TestServer.get_hide(db)


@router.post('/config')
async def config(mark: ConfigModel, db: Session = Depends(get_db)):
    return await TestServer.config(db)


@router.post("/restart", summary="软硬件重启")
async def restart_system(request: RestartRequest = Body(...)):
    # 重启类型 (software 或 hardware)
    return RebootService.restart_system(request.restart_type)
