import logging
import os
import sys
from datetime import timedelta
from hashlib import md5
from typing import Any, Dict, List, Tuple

from loguru import logger
from pydantic import PostgresDsn, SecretStr, RedisDsn
from fastapi_babel import Babel, BabelConfigs

from app.common.common import ROOT
from app.core.logging import InterceptHandler
from app.core.settings.base import BaseAppSettings
from app.core.settings.ini import CygnusConfig

# 配置psql数据库的连接信息
pg_ip, pg_port, pg_db_name, pg_username, pg_password, pg_scheme = CygnusConfig.get_psql_cfg()
# redis全局连接
redis_ip, redis_port, redis_db, redis_passwd = CygnusConfig.get_redis_cfg()
# i18n配置
translation_path = CygnusConfig.get_translation_cfg()


class AppSettings(BaseAppSettings):
    debug: bool = True
    docs_url: str = None
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    read_doc_url: str = "/read_doc"
    title: str = "CygnusS"
    version: str = "V.1"

    database_url: str = PostgresDsn.build(
                scheme=pg_scheme,
                username=pg_username,
                password=pg_password,
                host=pg_ip,
                port=pg_port,
                path=pg_db_name,
            )

    babel_configs: Any = BabelConfigs(
                ROOT_DIR=__file__,
                BABEL_DEFAULT_LOCALE="en",
                BABEL_TRANSLATION_DIRECTORY=translation_path,
            )

    redis_url: str = RedisDsn.build(
                scheme="redis",
                host=redis_ip,
                port=redis_port,
                password=redis_passwd,
                # database=redis_db,
            )

    max_pg_connection_count: int = 10
    min_pg_connection_count: int = 10

    max_redis_connection_count: int = 10
    min_redis_connection_count: int = 10

    secret_key: str = md5(os.urandom(24)).hexdigest()

    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "read_doc_url": self.read_doc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        # 设置日志文件保存 100 天
        log_retention = timedelta(days=100)

        # 配置文件日志
        logger.configure(handlers=[
            {
                "sink": os.path.join(ROOT, "logs\\app_{time:%Y-%m-%d}.log"),
                "level": self.logging_level,
                "retention": log_retention,
                "rotation": "1 day",
                "compression": "zip",
            }
        ])

        # 控制台输出日志
        logger.add(
            sys.stdout,
            level=self.logging_level
        )



