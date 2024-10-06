from datetime import datetime

from pydantic import BaseModel, condecimal, conint
from typing import List, Optional, Dict

from app.core.settings.base import RestartType, LogType


class ResponseTemplates(BaseModel):
    errno: int
    errmsg: str


# #############################  LogsController  #############################
class LogFile(BaseModel):
    file_name: str
    type: str
    date: str


class LogModules(BaseModel):
    python: List[LogFile] = []
    product: List[LogFile] = []
    go: List[LogFile] = []
    hardware: List[LogFile] = []
    fore_end: List[LogFile] = []


class ResponseModel(BaseModel):
    content: LogModules


class LogFilterParams(BaseModel):
    module_type: str
    level: Optional[str] = None
    start_date: Optional[str]  # 使用 datetime 类型来验证日期
    end_date: Optional[str]
    page_limit: conint(ge=1)  # 页大小必须大于等于 1
    current_page: conint(ge=1)  # 当前页数必须大于等于 1


class LogResponse(ResponseTemplates):
    errno:str
    errmsg:str
    data: Dict

class LogRequest(BaseModel):
    log_type: Optional[LogType] = None

class LogInfo(BaseModel):
    level: str
    message: str
    time: datetime

class LogResponseData(BaseModel):
    current_page: int
    log_info_list: List[LogInfo]
    total: int

class LogResponseModel(BaseModel):
    data: LogResponseData
    errmsg: str
    errno: str

class BackResponse(BaseModel):
    data: dict
    errmsg: str
    errno: str

class BackupRequest(BaseModel):
    type: str

class ExportResponse(BaseModel):
    errmsg: str
    errno: str

class ExportRequest(BaseModel):
    type: str
    task_ids: Optional[List[int]] = None

class TaskInfo(BaseModel):
    ID: Optional[int] = None
    box_slot: str
    create_time: str
    finish_time: Optional[str] = None
    failed_reason: Optional[str] = None
    is_audit: bool
    is_deleted_image: bool
    is_error: List[str]
    is_favorite: bool
    is_flatness: bool
    is_save: bool
    is_slide_out: bool
    patient_id: int
    patient_info: Optional[dict] = None
    patient_name: Optional[str] = None
    quality_percent: Optional[float] = None
    scan_parameter: Optional[str] = None
    scan_result: Optional[str] = None
    scan_type: str
    slide_id: str
    slide_slot: str
    status: str
    task_id: int
    ustretching_too_much: bool



class SearchRequest(BaseModel):
    current_page: int
    page_limit: int
    slide_id: str

# 定义响应模型
class SearchResponse(BaseModel):
    current_page: int
    task_info_dict_list: List[TaskInfo]
    total_count: int
    errmsg: str
    errno: str


# #############################  SysStatusController  #############################
class HardwareStatusModel(BaseModel):
    running_status: Optional[str] = None
    sensor_status: Optional[bool] = None

class HardwareStatusResponseModel(BaseModel):
    errno: Optional[str] = None
    data: HardwareStatusModel

class SensorStatusModel(BaseModel):
    status: bool

class SensorStatusResponseModel(BaseModel):
    errno: Optional[str] = None
    data: SensorStatusModel

class CommandOutputModel(BaseModel):
    info: Optional[str] = None



class CommandOutputResponseModel(BaseModel):
    errno: Optional[str] = None
    data: CommandOutputModel


class PythonServerModel(BaseModel):
    status: bool

class PythonServerResponseModel(BaseModel):
    errno: str
    data: PythonServerModel


class GoServerDataModel(BaseModel):
    status: bool

class GoServerResponseModel(BaseModel):
    errno: str
    data: GoServerDataModel



class SystemStatusModel(BaseModel):
    cpu_info: bool
    gpu_info: bool
    internal_storage: bool
    disk_info: Optional[str] = None  # 例如：80%
    memory_check: condecimal(max_digits=5, decimal_places=2)  # 例如：12.34%


class SysStatusResponseModel(BaseModel):
    errno: str
    errmsg: Optional[str] = None
    data: Optional[SystemStatusModel] = None

class WorkstationModel(BaseModel):
    cpu_info: Optional[bool] = None
    disk_info: Optional[str] = None
    gpu_info: Optional[bool] = None
    internal_storage: Optional[bool] = None


class ThirdModel(BaseModel):
    check_pytorch: Optional[bool] = None
    conn_redis: Optional[bool] = None
    conn_sql: Optional[bool] = None
    docker_info: Optional[bool] = None


class ModuleModel(BaseModel):
    algorithm_server: Optional[bool] = None
    go_server: Optional[bool] = None
    python_server: Optional[bool] = None
    write_server: Optional[bool] = None


class HardwareModel(BaseModel):
    running_status: Optional[str] = None
    sensor_status: Optional[bool] = None


class DataModel(BaseModel):
    hardware: Optional[HardwareModel] = None
    module: Optional[ModuleModel] = None
    third: Optional[ThirdModel] = None
    workstation: Optional[WorkstationModel] = None


class SystemStatusResponseModel(BaseModel):
    errno: str
    errmsg: Optional[str] = None
    data: Optional[DataModel] = None


# #############################  DataBack  #############################
class BackupData(BaseModel):
    dst_path: Optional[str] = None
    dst_name: Optional[List[str]] = None
    dst_folder: Optional[str] = None


class BackupResponse(BaseModel):
    errno: str
    errmsg: str
    data: Optional[BackupData] = None  # 将 data 字段设置为可选

    class Config:
        anystr_strip_whitespace = True


# #############################  HardwareController  #############################


class UAxisErrorCode(BaseModel):
    U_Cur_Position: Optional[int] = None
    U_Error_Code: Optional[str] = None  # 可以是字符串或者 None


class AxisState(BaseModel):
    X_Negative_Limit: Optional[bool] = None
    X_Command_Value: Optional[int] = None
    X_Encoder_Value: Optional[int] = None
    X_Positive_Limit: Optional[bool] = None

    Y_Negative_Limit: Optional[bool] = None
    Y_Command_Value: Optional[int] = None
    Y_Encoder_Value: Optional[int] = None
    Y_Positive_Limit: Optional[bool] = None

    S_Negative_Limit: Optional[bool] = None
    S_Command_Value: Optional[int] = None
    S_Positive_Limit: Optional[bool] = None


class ElectricalState(BaseModel):
    U: Optional[UAxisErrorCode] = None
    S: Optional[AxisState] = None
    X: Optional[AxisState] = None
    Y: Optional[AxisState] = None


class SensorState(BaseModel):
    Magzine_Load: Optional[bool] = None
    Slide: Optional[bool] = None
    Multiple_Slide: Optional[bool] = None


class ControlSwitchState(BaseModel):
    Fan_Switch: Optional[bool] = None
    _Pump_Switch: Optional[bool] = None
    Magzine_lock_Switch: Optional[bool] = None
    Light_Switch: Optional[bool] = None


class HardwareControllerData(BaseModel):
    System_Current_State: Optional[str] = None
    Sensor_State: Optional[SensorState] = None
    Control_Switch_State: Optional[ControlSwitchState] = None
    Electrical_State: Optional[ElectricalState] = None


class HardwareControllerResponse(BaseModel):
    errno: int
    errmsg: str
    data: Optional[HardwareControllerData] = None

    class Config:
        anystr_strip_whitespace = True


# #############################  CameraPictureController  #############################
class CameraPictureData(BaseModel):
    QRcameraPhoto: Optional[str] = None  # 将 QRcameraPhoto 设为可选的字符串


class CameraPictureResponse(BaseModel):
    errno: int
    errmsg: str
    data: Optional[CameraPictureData] = None  # 将 data 设为可选的字段

    class Config:
        anystr_strip_whitespace = True


# #############################  FinalVersionController  #############################
class FinalVersionData(BaseModel):
    software_python: Optional[str] = None
    software_ui: Optional[str] = None
    software_go: Optional[str] = None
    hardware: Optional[str] = None
    ALG_white: Optional[str] = None
    ALG_red: Optional[str] = None
    ALG_PC: Optional[str] = None
    release_num: Optional[str] = None


class FinalVersionControllerResponse(ResponseTemplates):
    data: FinalVersionData

    class Config:
        anystr_strip_whitespace = True


###########################  SetMarkHideController  #############################

# # ##
class SetMarkHideData(BaseModel):
    mark_file: Optional[str] = None
    mark_data: Optional[str] = None


class SetMarkHideControllerResponse(ResponseTemplates):
    data: Optional[dict] = None

    class Config:
        anystr_strip_whitespace = True


class ConfigModel(BaseModel):
    mark_data: Optional[bool] = True
    mark_file:Optional[bool] = True

class RestartRequest(BaseModel):
    restart_type: RestartType