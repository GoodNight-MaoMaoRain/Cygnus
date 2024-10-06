import traceback
from typing import Optional
from sqlalchemy.orm import Session
from loguru import logger
from app.common.response_code import RET
from fastapi_babel.core import _
from app.crud.crud_finalversion import CrudFinalVersion


class FinalVersionController:
    __instance = None

    @staticmethod
    def get_instance():
        if FinalVersionController.__instance is None:
            FinalVersionController.__instance = FinalVersionController()
        return FinalVersionController.__instance

    @staticmethod
    def final_version(session: Session, version_name: Optional[str] = None):
        try:
            try:
                if version_name:
                    logger.info(f'根据版本名称查询版本信息: {version_name}')
                    version_info = CrudFinalVersion.get_version_by_name(session, version_name)
                else:
                    logger.info('查询数据库中的第一个版本信息')
                    # 查询数据库中的第一个版本信息
                    version_info = CrudFinalVersion.get_final_version(session)
            except Exception:
                errmsg = f"获取部署版本信息失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.QueryFailed, "errmsg": _("获取部署版本信息失败"), "data": {}}

            if not version_info:
                errmsg = '数据库中没有找到版本信息。'
                logger.error(errmsg)
                return {"errno": RET.ReadCopyrightInfoFailed, "errmsg": _("数据库中没有找到版本信息。"), "data": {}}

            # 将查询到的数据放入字典
            patent_info_dic = {
                "software_python": version_info.software_python,
                "software_ui": version_info.software_ui,
                "software_go": version_info.software_go,
                "hardware": version_info.hardware,
                "ALG_white": version_info.alg_white,
                "ALG_red": version_info.alg_red,
                "ALG_PC": version_info.alg_pc,
                "release_num": version_info.release_num
            }

            logger.info('成功获取部署版本信息')

        except Exception:
            errmsg = f'读取部署版本信息失败: {traceback.format_exc()}'
            logger.error(errmsg)
            return {"errno": RET.ReadCopyrightInfoFailed, "errmsg": _("读取部署版本信息失败"), "data": {}}

        return {'errno': RET.OK, 'errmsg': _('OK'), "data": patent_info_dic}
