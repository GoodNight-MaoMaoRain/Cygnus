import traceback
from loguru import logger
from app.crud.crud_version_info import CRUDVersion
from app.schemas.schemas_super_engineer import VersionModel, VersionInfoModel
from app.common.response_code import RET
from fastapi_babel.core import _


class VersionAPI:
    def __init__(self, crud_version: CRUDVersion):
        # 初始化 CRUD 操作对象
        self.crud_version = crud_version

    def get_current_version(self) -> dict:
        try:
            logger.info("开始获取当前版本配置")
            # 从数据库中获取当前的版本配置
            try:
                version_config = self.crud_version.get_version_configuration()
            except Exception:
                errmsg = f"获取版本配置失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetVersionConfigFailed, "errmsg": _("获取版本配置失败"), "data": {}}

            version = version_config.project_version if version_config else None
            logger.info(f"当前版本为: {version}")
            return {"errno": RET.OK, "errmsg": _("获取成功"), "data": {"version": version}}

        except Exception:
            errmsg = f"获取当前版本失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.GetCurrentVersionFailed, "errmsg": _("获取当前版本失败"), "data": {}}

    def set_current_version(self, version_model: VersionModel) -> dict:
        try:
            logger.info("开始设置当前版本")
            # 从请求模型中获取要设置的版本名称
            version_name = version_model.version_name
            logger.info(f"请求设置的版本名称为: {version_name}")

            try:
                version_exists = self.crud_version.get_version_by_name(version_name)
                logger.info(f'版本查询结果：{version_exists}')
            except Exception:
                errmsg = f"检查版本是否存在失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetVersionInfoFailed, "errmsg": _("检查版本是否存在失败"), "data": {}}

            # 检查指定的版本是否存在
            if not version_exists:
                errmsg = "修改失败，版本不存在"
                logger.error(errmsg)
                return {"errno": RET.VersionNotFound, "errmsg": _("修改失败，版本不存在"), "data": {}}

            try:
                version_config = self.crud_version.get_version_configuration()
            except Exception:
                errmsg = f"获取版本配置失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetVersionConfigFailed, "errmsg": _("获取版本配置失败"), "data": {}}

            if not version_config:
                try:
                    version_config = self.crud_version.create_version_configuration()
                    logger.info("成功创建新版本配置")
                except Exception:
                    errmsg = f"创建版本配置失败: {traceback.format_exc()}"
                    logger.error(errmsg)
                    return {"errno": RET.CreateVersionConfigFailed, "errmsg": _("创建版本配置失败"), "data": {}}

            # 更新版本配置中的项目版本
            version_config.project_version = version_name

            try:
                new_info = {"project_version": version_name}
                self.crud_version.update_version_info(version_config, new_info)
                logger.info(f"版本信息已更新: {new_info}")
            except Exception:
                errmsg = f"更新版本信息失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.UpdateVersionInfoFailed, "errmsg": _("更新版本信息失败"), "data": {}}

            logger.info(f"版本信息设置成功: {version_config.project_version}")
            return {"errno": RET.OK, "errmsg": _("修改成功"), "data": {"version": version_config.project_version}}

        except Exception:
            errmsg = f"设置当前版本失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.SetCurrentVersionFailed, "errmsg": _("设置当前版本失败"), "data": {}}

    def get_current_version_info(self) -> dict:
        try:
            logger.info("开始获取当前版本信息")
            # 获取当前的版本配置
            try:
                version_config = self.crud_version.get_version_configuration()
            except Exception:
                errmsg = f"获取版本配置失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetVersionInfoFailed, "errmsg": _("获取版本配置失败"), "data": {}}

            if not version_config:
                errmsg = "未找到版本配置"
                logger.error(errmsg)
                return {"errno": RET.CurrentVersionNotSet, "errmsg": _("查看失败，未找到版本配置"), "data": {}}

            try:
                current_version = self.crud_version.get_version_info_by_name(version_config.project_version)
            except Exception:
                errmsg = f"获取版本信息失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetVersionInfoFailed, "errmsg": _("获取版本信息失败"), "data": {}}

            if not current_version:
                errmsg = "当前版本未设置"
                logger.error(errmsg)
                return {"errno": RET.CurrentVersionNotSet, "errmsg": _("查看失败，当前版本未设置"), "data": {}}

            version_info = VersionInfoModel(
                software_python=current_version.software_python,
                software_ui=current_version.software_ui,
                software_go=current_version.software_go,
                hardware=current_version.hardware,
                ALG_white=current_version.alg_white,
                ALG_red=current_version.alg_red,
                ALG_pc=current_version.alg_pc,
                release_num=current_version.release_num,
            )
            logger.info("版本信息获取成功")
            return {"errno": RET.OK, "errmsg": _("查看成功"), "data": version_info.model_dump()}

        except Exception:
            errmsg = f"获取版本信息失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.GetVersionInfoFailed, "errmsg": _("获取版本信息失败"), "data": {}}

    def set_current_version_info(self, new_info: VersionInfoModel) -> dict:
        try:
            logger.info("开始设置当前版本信息")
            # 获取当前的版本配置
            try:
                version_config = self.crud_version.get_version_configuration()
            except Exception:
                errmsg = f"获取版本配置失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetVersionInfoFailed, "errmsg": _("获取版本配置失败"), "data": {}}

            if not version_config:
                errmsg = "修改版本信息失败，未找到版本配置"
                logger.error(errmsg)
                return {"errno": RET.SetVersionInfoFailed, "errmsg": _("修改版本信息失败，未找到版本配置"), "data": {}}

            try:
                current_version = self.crud_version.get_version_info_by_name(version_config.project_version)
            except Exception:
                errmsg = f"获取当前版本信息失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.GetVersionInfoFailed, "errmsg": _("获取当前版本信息失败"), "data": {}}

            if not current_version:
                errmsg = "当前版本未设置"
                logger.error(errmsg)
                return {"errno": RET.CurrentVersionNotSet, "errmsg": _("查看失败，当前版本未设置"), "data": {}}

            new_info_dict = new_info.model_dump()
            logger.info(f"新版本信息: {new_info_dict}")

            try:
                self.crud_version.update_version_info(current_version, new_info_dict)
            except Exception:
                errmsg = f"更新版本信息失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.UpdateVersionInfoFailed, "errmsg": _("更新版本信息失败"), "data": {}}

            return {"errno": RET.OK, "errmsg": _("修改成功, 当前版本信息已更新"), "data": new_info_dict}

        except Exception:
            errmsg = f"设置版本信息失败: {traceback.format_exc()}"
            logger.error(errmsg)
            return {"errno": RET.SetVersionInfoFailed, "errmsg": _("设置版本信息失败"), "data": {}}
