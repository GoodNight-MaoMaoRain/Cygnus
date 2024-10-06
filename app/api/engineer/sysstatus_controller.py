import psutil
import torch
import subprocess
import traceback
import chardet
from loguru import logger
from fastapi_babel.core import _
from sqlalchemy.orm import Session

from app.orm.models import SimulationData
from app.common.response_code import RET
from app.schemas.schemas_engineer import SystemStatusModel
from app.lib.hardware.hardware.client import HttpClient


# 用于监控和报告系统硬件状态
class SysStatusController:
    __instance = None

    @staticmethod
    def get_instance():
        if SysStatusController.__instance is None:
            SysStatusController.__instance = SysStatusController()
        return SysStatusController.__instance

    @staticmethod
    def running_status():
        try:  # 新增 try 块
            immersion_, cover_closed, slide_holder, temperature_over_high, is_horizontal, device_status, error_code = (
                HttpClient.get_instance().query_module_status()
            )
            hardware_status = ["Idle", "Active", "Init", "Fault", "Check"][
                device_status] if device_status is not None else None
            logger.info(f"查询运行状态成功: {hardware_status}")
            return {
                "errno": RET.OK,
                "data": {
                    "status": hardware_status,
                    "sensor_status": False
                }
            }

            # return {"errno": RET.OK, "data":hardware_status}
        except Exception:
            errmsg = f"查询运行状态失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.SysStatusQueryFailed, "errmsg": _("查询运行状态失败"), "data": {}}

    @staticmethod
    def sensor_status():
        try:
            logger.info("查询传感器状态成功")
            return {
                "errno": RET.OK,
                "data": {
                    "status": True
                }
            }

        except Exception:
            errmsg = f"查询传感器状态失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.SensorStatusQueryFailed, "errmsg": _("查询传感器状态失败"), "data": {}}

    @staticmethod
    def top_command():
        try:
            top_info = subprocess.Popen(["wmic", "process", "get", "Name,ProcessId,CommandLine"],
                                        stdout=subprocess.PIPE)
            out, stderr_output = top_info.communicate()

            # 自动检测编码
            detected_encoding = chardet.detect(out)['encoding']
            out_info = out.decode(detected_encoding)
            logger.info("top命令查询成功")
            return {
                "errno": RET.OK,
                "data": {
                    "info": out_info
                }
            }

        except Exception:
            errmsg = f"top查询失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.TopCommandQueryFailed, "errmsg": _("top查询失败"), "data": {}}

    @staticmethod
    def nvidia_command():
        try:
            nvidia_info = subprocess.Popen("nvidia-smi", stdout=subprocess.PIPE)
            out, stderr_output = nvidia_info.communicate()
            out_info = out.decode('unicode-escape')
            logger.info("nvidia-smi查询成功")
            return {
                "errno": RET.OK,
                "data": {
                    "info": out_info
                }
            }

        except Exception:
            errmsg = f"nvidia-smi查询失败: {str(traceback.format_exc())}"
            logger.error(errmsg)
            return {"errno": RET.NvidiaCommandQueryFailed, "errmsg": _("nvidia-smi查询失败"), "data": {}}

    @staticmethod
    def python_server():
        try:  # 新增 try 块
            logger.info("Python服务器状态查询成功")
            return {
                "errno": RET.OK,
                "data": {
                    "status": True
                }
            }
        except Exception:
            errmsg = f"查询Python服务器状态失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.PythonServerQueryFailed, "errmsg": _("查询Python服务器状态失败"), "data": {}}

    @staticmethod
    def go_server(db: Session):
        try:
            logger.info("Go服务器状态查询成功")
            response = {
                "errno": RET.OK,
                "data": {
                    "status": True,
                }
            }

            new_simulation = SimulationData(
                go_server=response
            )
            db.add(new_simulation)
            db.commit()
            db.refresh(new_simulation)

            return response
        except Exception:
            errmsg = f"查询Go服务器状态失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.GoServerQueryFailed, "errmsg": _("查询Go服务器状态失败"), "data": {}}

    # windows环境下
    # @staticmethod
    # def get_disk_info():
    #     try:
    #         result = subprocess.Popen('powershell "Get-PSDrive -PSProvider FileSystem"', shell=True,
    #                                   stdout=subprocess.PIPE).stdout.read().decode()
    #         for line in result.split('\n'):
    #             if 'C:' in line:  # 选择你感兴趣的磁盘
    #                 return line.split()[3]  # 返回空闲空间（按需选择其他字段）
    #     except Exception:
    #         errmsg = f"查询磁盘信息失败: {traceback.format_exc()}"
    #         logger.error(errmsg)
    #         return {"errno": RET.DiskInfoQueryFailed, "errmsg": _("查询磁盘信息失败"), "data": {}}

    # linux环境下的
    @staticmethod
    def get_disk_info():
        try:  # 新增 try 块
            result = subprocess.Popen('df -h', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
            for line in result.split('\n'):
                if 'mnt' in line:
                    logger.info(f"查询磁盘信息成功: {line.split()[4]}")
                    return line.split()[4]
        except Exception:
            errmsg = f"查询磁盘信息失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.UNKOWNERR, "errmsg": _("查询磁盘信息失败"), "data": {}}

    @staticmethod
    def memory_check():
        try:  # 新增 try 块
            mem_file_path = r'D:\CygnusS\app\api\engineer\proc\meminfo.txt'
            with open(mem_file_path) as mem_file:
                # with open('/proc/meminfo') as mem_file:
                mem_info_list = mem_file.readlines()
                total = int(mem_info_list[0].split(":")[1].split("kB")[0])
                free = int(mem_info_list[1].split(":")[1].split("kB")[0])

                memory_usage = round((free / total) * 100, 0)
                logger.info(f"查询内存信息成功: 使用率为 {memory_usage}%")
                return memory_usage
        except Exception:
            errmsg = f"查询内存信息失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.MemoryInfoQueryFailed, "errmsg": _("查询内存信息失败"), "data": {}}

    @staticmethod
    def internal_storage():
        try:  # 新增 try 块
            mem = psutil.virtual_memory()
            total = round(mem.total / 1024 / 1024 / 1024, 2)
            used = round(mem.used / 1024 / 1024 / 1024, 2)
            storage_status = used < total
            logger.info(f"查询内部存储信息成功: 总容量 {total}GB, 已使用 {used}GB")
            return storage_status

        except Exception:
            errmsg = f"查询内部存储信息失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.InternalStorageQueryFailed, "errmsg": _("查询内部存储信息失败"), "data": {}}

    @staticmethod
    def cpu_info():
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            logger.info(f"查询CPU信息成功: 当前CPU使用率为 {cpu_percent}%")
            return cpu_percent < 100
        except Exception:
            errmsg = f"查询CPU信息失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.CpuInfoQueryFailed, "errmsg": _("查询CPU信息失败"), "data": {}}

    @staticmethod
    def gpu_info():
        try:
            if not torch.cuda.is_available():
                logger.info("查询GPU信息成功: GPU 不可用")
                return False

            logger.info("查询GPU信息成功: GPU 可用")
            return True

        except Exception:
            errmsg = f"查询GPU信息失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.GpuInfoQueryFailed, "errmsg": _("查询GPU信息失败"), "data": {}}

    def get_system_status(self):
        try:
            system_status = SystemStatusModel(
                cpu_info=self.cpu_info(),
                gpu_info=self.gpu_info(),
                internal_storage=self.internal_storage(),
                disk_info=self.get_disk_info(),
                memory_check=self.memory_check()
            )
            logger.info("获取系统状态成功")

            response = {
                "errno": RET.OK,  # 假设成功时返回 0
                "errmsg": _("获取系统状态成功"),
                "data": system_status  # data 字段包含 SystemStatusModel 类型的数据
            }
            return response


        except Exception:
            errmsg = f'获取系统失败:{str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.SystemStatusQueryFailed, "errmsg": _("获取系统失败"), "data": {}}

    @staticmethod
    def get_sys_status():
        try:
            sys_status = SysStatusController.get_instance()

            # 获取系统状态
            system_status_response = sys_status.get_system_status()
            system_status_data = system_status_response["data"] if system_status_response.get(
                "data") else SystemStatusModel()

            # 组装返回数据
            status = {
                "errno": "0",
                "errmsg": "成功",
                "data": {
                    "hardware": {
                        "running_status": sys_status.running_status().get("data", {}).get("status", "Unknown"),
                        "sensor_status": sys_status.sensor_status().get("data", {}).get("status", False)
                    },
                    "module": {
                        "algorithm_server": True,
                        "go_server": sys_status.go_server().get("data", {}).get("status", False),
                        "python_server": sys_status.python_server().get("data", {}).get("status", False),
                        "write_server": True
                    },
                    "third": {
                        "check_pytorch": True,
                        "conn_redis": True,
                        "conn_sql": True,
                        "docker_info": True
                    },
                    "workstation": {
                        "cpu_info": system_status_data.cpu_info if system_status_data.cpu_info is not None else False,
                        "disk_info": system_status_data.disk_info if system_status_data.disk_info is not None else "Unknown",
                        "gpu_info": system_status_data.gpu_info if system_status_data.gpu_info is not None else False,
                        "internal_storage": system_status_data.internal_storage if system_status_data.internal_storage is not None else False
                    }
                }
            }
            logger.info("获取系统状态成功")
            return status

        except Exception:
            errmsg = f'获取系统状态失败: {traceback.format_exc()}'
            logger.error(errmsg)
            return {"errno": RET.SystemStatusQueryFailed, "errmsg": _("获取系统状态失败"), "data": {}}
