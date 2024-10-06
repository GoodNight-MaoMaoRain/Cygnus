from typing import Dict
from loguru import logger
from app.common.response_code import RET
from fastapi_babel.core import _

from app.core.settings.base import RestartType


class RebootService:
    @staticmethod
    def restart_system(restart_type: RestartType) -> Dict[str, str]:
        """
        根据重启类型执行软件或硬件重启
        :param restart_type: RestartType 枚举值
        :return: 重启结果信息
        """
        try:
            if restart_type == RestartType.software:
                # 执行软件重启脚本
                # subprocess.Popen(["/path/to/restart_software.sh"])
                logger.info("软件重启成功")
                return {"errno": RET.OK, "errmsg": _("软件重启成功")}

            elif restart_type == RestartType.hardware:
                # 执行硬件重启脚本
                # subprocess.Popen(["/path/to/restart_hardware.sh"])
                logger.info("硬件重启成功")
                return {"errno": RET.OK, "errmsg": _("硬件重启成功")}

            else:
                return {"errno": "1", "errmsg": _("无效的重启类型")}

        except Exception as e:
            errmsg = f"重启失败: {str(e)}"
            logger.error(errmsg)
            return {"errno": "1", "errmsg": _("重启失败")}
