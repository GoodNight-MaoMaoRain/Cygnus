import traceback
from loguru import logger
from app.crud.crud_i18n import CRUDI18N
from app.crud.crud_version_info import CRUDVersion
from app.schemas.schemas_super_engineer import UpdateLanguageRequest
from app.common.response_code import RET
from fastapi_babel.core import _
import json


class I18NAPI:
    def __init__(self, crud_i18n: CRUDI18N, crud_version: CRUDVersion):
        self.crud_i18n = crud_i18n
        self.crud_version = crud_version

    def get_current_language(self) -> dict:
        try:
            logger.info("开始获取当前语言信息")
            # 从数据库获取当前语言
            try:
                i18n = self.crud_i18n.get_current_language()
                logger.info(f"成功获取当前语言: {i18n.language_code if i18n else 'None'}")
            except Exception:
                errmsg = f'获取当前语言失败:{traceback.format_exc()}'
                logger.error(errmsg)
                return {
                    "errno": RET.GetCurrentLanguageFailed,
                    "errmsg": _("获取当前语言失败"),
                    "data": {}
                }

            # 如果数据库中没有相关记录，使用默认值 'zh' 并创建记录
            if not i18n:
                try:
                    self.crud_i18n.create_default_language()
                    logger.info("创建默认语言记录成功，默认语言设置为 'zh'")

                except Exception:
                    errmsg = f'创建默认语言记录失败:{traceback.format_exc()}'
                    logger.error(errmsg)

                    return {
                        "errno": RET.CreateDefaultLanguageFailed,
                        "errmsg": _("创建默认语言记录失败"),
                        "data": {}
                    }

            # 获取当前的版本信息
            try:
                current_version = self.crud_version.get_version_configuration()
                version = current_version.project_version if current_version else None
                logger.info(f"当前版本信息: {version}")

            except Exception:
                errmsg = f'获取当前版本配置失败:{traceback.format_exc()}'
                logger.error(errmsg)
                return {
                    "errno": RET.GetCurrentVersionFailed,
                    "errmsg": _("获取当前版本配置失败"),
                    "data": {}
                }

            # 处理 select_languages 和 language_code
            try:
                select_languages = json.loads(i18n.select_languages)
                logger.info(f"解析 select_languages 成功: {select_languages}")

            except Exception:
                errmsg = f'解析 select_languages 失败:{traceback.format_exc()}'
                logger.error(errmsg)

                return {
                    "errno": RET.ParseSelectLanguagesFailed,
                    "errmsg": _("解析 select_languages 失败"),
                    "data": {}
                }
            # 对象属性的读取操作
            language_code = i18n.language_code
            logger.info(f"语言代码: {language_code}")

            data = {
                "language_code": language_code,
                "select_languages": select_languages,
                "current_version": version
            }

            # 返回 language_code, select_languages 和当前版本信息
            logger.info("成功获取当前语言信息和版本信息")
            return {
                "errno": RET.OK,
                "errmsg": _("获取成功"),
                "data": data
            }

        except Exception:
            errmsg = f'获取当前语言失败:{traceback.format_exc()}'
            logger.error(errmsg)
            return {
                "errno": RET.GetLanguageInfoFailed,
                "errmsg": _("获取语言信息失败"),
                "data": {}
            }

    def set_language(self, language_request: UpdateLanguageRequest) -> dict:
        try:
            language_code = language_request.language
            logger.info(f"开始设置语言: {language_code}")

            try:
                i18n = self.crud_i18n.get_current_language()
                logger.info(f"当前语言记录: {i18n.language_code if i18n else 'None'}")

            except Exception:
                errmsg = f'获取当前语言失败:{traceback.format_exc()}'
                logger.error(errmsg)
                return {
                    "errno": RET.GetLanguageRecordFailed,
                    "errmsg": _("获取当前语言记录失败"),
                    "data": {}
                }

            # 如果没有记录则创建新的
            if not i18n:
                try:
                    self.crud_i18n.create_default_language()
                    logger.info("创建默认语言记录成功")

                except Exception:
                    errmsg = f'创建默认语言记录失败:{traceback.format_exc()}'
                    logger.error(errmsg)
                    return {
                        "errno": RET.CreateDefaultLanguageFailed,
                        "errmsg": _("创建默认语言记录失败"),
                        "data": {}
                    }

            # 检查语言是否在允许的列表中
            try:
                available_languages = json.loads(i18n.select_languages)
                logger.info(f"允许的语言列表: {available_languages}")

                if language_code not in available_languages:
                    errmsg = '语言不在允许的列表中'
                    logger.error(f"{errmsg}: {language_code}")
                    return {"errno": RET.LanguageNotAllowed, "errmsg": _("语言不在允许的列表中"), "data": {}}

            except Exception:
                errmsg = f'解析 select_languages 失败:{traceback.format_exc()}'
                logger.error(errmsg)

                return {
                    "errno": RET.ParseSelectLanguagesFailed,
                    "errmsg": _("解析 select_languages 失败"),
                    "data": {}
                }

            try:

                self.crud_i18n.update_language(i18n,language_code)
                logger.info(f"语言记录更新成功: {language_code}")

            except Exception:
                errmsg = f'更新语言记录失败:{traceback.format_exc()}'
                logger.error(errmsg)
                return {
                    "errno": RET.UpdateLanguageFailed,
                    "errmsg": _("更新语言记录失败"),
                    "data": {}
                }

            return {"errno": RET.OK, "errmsg": _("语言修改成功"), "data": {"language": language_code}}

        except Exception:

            errmsg = f'设置语言失败: {traceback.format_exc()}'
            logger.error(errmsg)

            return {
                "errno": RET.SetLanguageFailed,
                "errmsg": _("设置语言失败"),
                "data": {}
            }
