import traceback
from loguru import logger
from sqlalchemy.orm import Session
from app.orm.models import SimulationData
from app.common.response_code import RET
from fastapi_babel.core import _


# 用于管理和监控硬件状态的控制器
class HardwareController:
    __instance = None

    @staticmethod
    def get_instance():
        if HardwareController.__instance is None:
            HardwareController.__instance = HardwareController()
        return HardwareController.__instance

    @staticmethod
    def get_Uaxis_code():
        try:
            # U轴报警代码
            Uaxis_code = {
                "0x2300": "电机过流",
                "0x2311": "电机过载",
                "0x2312": "电机堵转",
                "0x3210": "电源过电压",
                "0x3220": "电源欠电压",
                "0x4210": "温度过高报警",
                "0x4220": "温度过低报警",
                "0x5080": "驱动器故障*",
                "0x5540": "Flash操作故障*",
                "0x5541": "Flash初始化故障*",
                "0x5542": "Flash校验错误警告*",
                "0x5543": "Flash用户区无参数*",
                "0x5544": "掉电位置存储异常",
                "0x5545": "掉电保存数据未存储",
                "0x6000": "硬件初始化故障*",
                "0x6320": "参数设置错误",
                "0x6321": "注册故障*",
                "0x7305": "Z脉冲故障*",
                "0x7306": "编码器故障*",
                "0x7307": "编码器警告*",
                "0x7310": "超速",
                "0x7501": "Modbus通信中的非法功能码",
                "0x7502": "Modbus通信中的非法地址",
                "0x7503": "Modbus通信中的非法数据值",
                "0x7505": "Modbus通信中的确认",
                "0x7506": "Modbus通信中的从设备忙",
                "0x750C": "Modbus通信中的同步报文请求数据数据大于映射总数据",
                "0x750D": "Modbus 通信中的同步报文请求数据个数对应映射数据不相等",
                "0x750E": "Modbus通信中的同步功能下单播报文节点地址错误",
                "0x8311": "限扭矩保护",
                "0x8610": "原点回归超时",
                "0x8611": "位置超差",
                "0x8613": "软件限位错误",
                "0x8614": "限位开关错误",
                "0x8615": "曲线规划计算错误",
                "0x8616": "目标位置溢出",
                "0x8617": "曲线规划参数过小",
                "0xFF01": "电机参数识别故障*",
                "0xFF02": "参数保存故障"
            }
            return Uaxis_code
        except Exception:
            errmsg = f"获取U轴报警代码失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.GetUaxisCodeFailed, "errmsg": "获取U轴报警代码失败"}

    @staticmethod
    def get_sys_code():
        try:
            # 系统运行步骤说明
            sys_code = {

                "idle": "空闲",
                "AllMotorGoHome": "电机回原点进行中",
                "XYMegazinePosition": "XY运动到进片位置行进中",
                "MultipleSlideDetection": "多片检测进行中",
                "SlideInPhoto": "进片操作1-拍照进行中",
                "SlideIn": "进片操作2-滴油进行中",
                "SlideInScanPosition": "进片操作3-运动到扫描位置进行中",
                "UMotorWait": "U轴电机回到待机位置，等待扫描结束中",
                "HookUpPosition": "扫描完毕，运动到待上钩位置进行中",
                "HookUp": "上钩进行中",
                "SlideOutSensorPosition": "出片操作1-运动到玻片传感器位置进行中",
                "SlideOutMegazine": "出片操作2-玻片放回玻片盒进行中",
                "Unhook": "脱钩进行中"

            }
            return sys_code
        except Exception:
            errmsg = f"获取系统运行代码失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.GetSysCodeFailed, "errmsg": "获取系统运行代码失败"}

    def running_hardware_status(self, db: Session):
        """
            获取硬件状态信息，查询下位机硬件状态上报
        """

        try:
            # 正式请求
            # hardware_status_data = HttpClient.get_instance().query_hardware_status()

            # 模拟数据
            hardware_status_data = {
                "result": "Success",
                "X_Command_Value": 265845,
                "X_Encoder_Value": 87247,
                "Y_Command_Value": 165153,
                "Y_Encoder_Value": 104523,
                "S_Command_Value": 16569,
                "U_Cur_Position": 76894,
                "U_Error_Code": "0x8610",
                "X_Positive_Limit": False,
                "X_Negative_Limit": False,
                "Y_Positive_Limit": False,
                "Y_Negative_Limit": False,
                "S_Positive_Limit": False,
                "S_Negative_Limit": False,
                "System_Current_State": "idle",
                "Slide": True,
                "Multiple_Slide": True,
                "Magzine_Load": True,
                "Magzine_lock_Switch": True,
                "Light_Switch": True,
                "_Pump_Switch": False,
                "Fan_Switch": False
            }

        except Exception:
            errmsg = f"获取硬件模块状态失败: {traceback.format_exc()}"
            logger.error(errmsg)
            # X
            return {"errno": RET.GetHardwareStatusFailed, "errmsg": _("获取硬件模块状态失败")}

        if hardware_status_data:
            try:  # 新增 try 块
                data = {}

                # 系统状态
                data["System_Current_State"] = self.get_sys_code().get(hardware_status_data.get("System_Current_State"))

                # 传感器状态
                data["Sensor_State"] = {

                    # 玻片盒检测: 有玻片盒：true，无玻片盒：false
                    "Magzine_Load": hardware_status_data.get("Magzine_Load"),
                    # 玻片传感器: 有玻片：true，无玻片：false
                    "Slide": hardware_status_data.get("Slide"),
                    # 多片检测传感器: 有玻片：true，无玻片：false
                    "Multiple_Slide": hardware_status_data.get("Multiple_Slide")

                }

                # 控制开关状态
                data["Control_Switch_State"] = {

                    # 风扇开关状态: 开：true，关：false
                    "Fan_Switch": hardware_status_data.get("Fan_Switch"),
                    # 油泵开关状态: 开：true，关：false
                    "_Pump_Switch": hardware_status_data.get("_Pump_Switch"),
                    # 电磁阀开关状态: 开：true，关：false
                    "Magzine_lock_Switch": hardware_status_data.get("Magzine_lock_Switch"),
                    # 光源开关状态: 开：true，关：false
                    "Light_Switch": hardware_status_data.get("Light_Switch"),
                }

                # 电机状态
                data["Electrical_State"] = {
                    # U轴
                    "U": {

                        # U轴当前用户位置绝对反馈: 例如：76894
                        "U_Cur_Position": hardware_status_data.get("U_Cur_Position"),
                        # U轴错误码: 例如：34320（0x8610）原点回归超时，详见附表4.2
                        "U_Error_Code": self.get_Uaxis_code().get(hardware_status_data.get("U_Error_Code")),
                    },
                    # S轴
                    "S": {

                        # S-限位: 触发：true，未触发：false
                        "S_Negative_Limit": hardware_status_data.get("S_Negative_Limit"),
                        # S轴脉冲值: 例如：16569
                        "S_Command_Value": hardware_status_data.get("S_Command_Value"),
                        # S+限位: 触发：true，未触发：false
                        "S_Positive_Limit": hardware_status_data.get("S_Positive_Limit")

                    },

                    # X轴
                    "X": {
                        # X-限位: 触发：true，未触发：false
                        "X_Negative_Limit": hardware_status_data.get("X_Negative_Limit"),
                        # X轴脉冲值: 例如：265845
                        "X_Command_Value": hardware_status_data.get("X_Command_Value"),
                        # X轴光栅尺示数: 例如：87247
                        "X_Encoder_Value": hardware_status_data.get("X_Encoder_Value"),
                        # X+限位: 触发：true，未触发：false
                        "X_Positive_Limit": hardware_status_data.get("X_Positive_Limit"),

                    },

                    # Y轴
                    "Y": {

                        # Y-限位: 触发：true，未触发：false
                        "Y_Negative_Limit": hardware_status_data.get("Y_Negative_Limit"),
                        # Y轴脉冲值: 例如：165153
                        "Y_Command_Value": hardware_status_data.get("Y_Command_Value"),
                        # Y轴光栅尺示数: 例如：104523
                        "Y_Encoder_Value": hardware_status_data.get("Y_Encoder_Value"),
                        # Y+限位: 触发：true，未触发：false
                        "Y_Positive_Limit": hardware_status_data.get("Y_Positive_Limit"),

                    }
                }

                new_simulation = SimulationData(
                    hardware_status=data
                )
                db.add(new_simulation)
                db.commit()
                db.refresh(new_simulation)

                return {"errno": RET.OK, "errmsg": _("成功"), "data": data}
            except Exception:
                errmsg = f"处理硬件状态数据失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.ProcessHardwareStatusDataFailed, "errmsg": _("处理硬件状态数据失败")}

        else:
            errmsg = f'获取硬件模块状态失败:{str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.GetHardwareStatusFailed, "errmsg": _("获取硬件模块状态失败")}
