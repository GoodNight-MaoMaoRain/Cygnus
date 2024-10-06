from sqlalchemy.orm import Session
from typing import Optional
from loguru import logger
from app.orm.models import VersionConfiguration, VersionInfo
import json

class CRUDVersion:
    def __init__(self, db: Session):
        self.db = db

    def get_version_configuration(self) -> Optional[VersionConfiguration]:
        """
        从数据库中获取版本配置。
        """
        return self.db.query(VersionConfiguration).first()

    def get_version_info_by_name(self, version_name: str) -> Optional[VersionInfo]:
        """
        根据版本名称从数据库中获取版本信息。
        """
        # 获取版本配置
        version_config = self.db.query(VersionConfiguration).first()

        if not version_config:
            logger.error("未找到版本配置")
            return None

        # 获取 select_versions 并加载为字典
        select_versions = json.loads(version_config.select_versions)
        logger.info(f"select_versions 内容: {select_versions}")

        # 检查 version_name 是否存在于 select_versions 的键中
        if version_name in select_versions:
            logger.info(f"版本 {version_name} 存在于 select_versions 中")
            # **从数据库查询 VersionInfo 表中是否存在对应版本**
            version_info = self.db.query(VersionInfo).filter(VersionInfo.version_name == version_name).first()

            if version_info:
                return version_info
            else:
                logger.error(f"未在 VersionInfo 表中找到版本 {version_name}")
                return None

        logger.error(f"版本 {version_name} 不存在于 select_versions 中")
        return None

    def get_version_by_name(self, version_name: str) -> Optional[VersionInfo]:
        """
        根据版本名称从数据库中获取版本信息。
        """
        # 获取版本配置
        version_config = self.db.query(VersionConfiguration).first()

        if not version_config:
            logger.error("未找到版本配置")
            return None

        # 获取 select_versions 并加载为字典
        select_versions = json.loads(version_config.select_versions)
        logger.info(f"select_versions 内容: {select_versions}")

        # 检查 version_name 是否存在于 select_versions 的键中
        if version_name in select_versions:
            logger.info(f"版本 {version_name} 存在于 select_versions 中")
            # 查询 VersionInfo 表中是否存在对应版本
            return VersionInfo(version_name=version_name)

        logger.error(f"版本 {version_name} 不存在于 select_versions 中")
        return None


    def update_version_info(self, current_version: VersionInfo, new_info: dict):
        """
        更新数据库中的版本信息。
        """
        for key, value in new_info.items():
            setattr(current_version, key.lower(), value)
        self.db.commit()
        self.db.refresh(current_version)

    def create_version_configuration(self) -> VersionConfiguration:
        """
        创建并保存一个新的版本配置实例。
        """
        version_config = VersionConfiguration()
        self.db.add(version_config)
        self.db.commit()
        self.db.refresh(version_config)
        return version_config
