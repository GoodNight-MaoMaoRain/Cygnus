import os
import json
import datetime
import subprocess
import traceback

from loguru import logger
from fastapi import BackgroundTasks
from app.common.common import DOWNLOADS_PATH
from app.common.response_code import RET
from app.core.settings.ini import CygnusConfig
from fastapi_babel.core import _
# from app.orm.models import InsertDB


# 数据库备份和任务数据导出
class DataBack:
    """
    数据库备份
    """
    __instance = None

    @staticmethod
    def get_instance():
        if DataBack.__instance is None:
            DataBack.__instance = DataBack()
        return DataBack.__instance

    def export_postgres_db(self, host: str, port: int, username: str, password: str, database: str, output_file: str):
        """
        导出 PostgreSQL 数据库
        """
        pg_dump_cmd = [
            'pg_dump',
            f'--host={host}',
            f'--port={port}',
            f'--username={username}',
            f'--dbname={database}',
            f'--file={output_file}',
            '--no-password'
        ]

        # 使用PGPASSWORD环境变量提供密码
        if password:
            os.environ['PGPASSWORD'] = password

        try:
            logger.info(f'开始执行 pg_dump 命令: {" ".join(pg_dump_cmd)}')
            subprocess.run(pg_dump_cmd, check=True)
            logger.info('数据库备份成功')
        except subprocess.CalledProcessError:
            errmsg = f'pg_dump 命令执行失败: {traceback.format_exc()}'
            logger.error(errmsg)
            return {"errno": RET.DBUpdateError, "errmsg": _("数据库备份失败"), "data": {}}

    def sql_back_data(self):
        """
        导出数据库数据
        """
        try:
            pg_ip, pg_port, pg_db_name, pg_username, pg_password = CygnusConfig.get_psql_cfg()
            backup_file = f'{pg_db_name}_backup_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.sql'
            backup_path = os.path.join(DOWNLOADS_PATH, backup_file)

            try:
                logger.info(f'开始导出 PostgreSQL 数据库到: {backup_path}')
                self.export_postgres_db(pg_ip, pg_port, pg_username, pg_password, pg_db_name, backup_path)
            except Exception:
                errmsg = f'导出 PostgreSQL 数据库失败: {traceback.format_exc()}'
                logger.error(errmsg)
                return {"errno": RET.DBQueryError, "errmsg": _("导出数据库失败")}

            return {"errno": RET.OK, "errmsg": "成功", "data": {"dst_path": DOWNLOADS_PATH}}

        except Exception:
            errmsg = f'导出数据库失败: {traceback.format_exc()}'
            logger.error(errmsg)
            return {"errno": RET.DBQueryError, "errmsg": "导出数据库失败"}

    #  export_task_data 后加的
    def export_task_data(self, dst_folder_path: str, task_ids: list):
        """
        将任务数据导出到指定的文件夹
        """
        try:
            # 这里添加导出任务数据的逻辑
            # 示例：将任务 ID 列表写入一个文件
            export_file_path = os.path.join(dst_folder_path, "task_data.json")
            with open(export_file_path, "w") as f:
                json.dump(task_ids, f)
            logger.info(f"任务数据成功导出到: {export_file_path}")
        except Exception:
            errmsg = f'导出任务数据失败: {traceback.format_exc()}'
            logger.error(errmsg)
            return {"errno": RET.TaskExportError, "errmsg": _("导出任务数据失败")}

    def task_back_data(self, task_ids: str, background_tasks: BackgroundTasks):
        """
        导出任务数据并保存到数据库
        """
        dst_folder_path = DOWNLOADS_PATH
        task_ids = json.loads(task_ids)

        try:
            # 将任务导出任务放到后台任务中
            try:
                logger.info(f'添加后台任务以导出任务数据: {task_ids}')
                background_tasks.add_task(self.export_task_data, dst_folder_path, task_ids)
            except Exception:
                errmsg = f'后台任务添加失败: {traceback.format_exc()}'
                logger.error(errmsg)
                return {"errno": RET.TaskAddError, "errmsg": _("后台任务添加失败"), "data": {}}

            # 将数据导出到数据库
            db_path = os.path.join(dst_folder_path, "yuetu.db")
            try:
                logger.info(f'将任务数据导出到数据库: {db_path}')
                res = InsertDB(db_path).into_db(task_ids)
                if not res:
                    errmsg = f'导出任务DB数据库失败: {traceback.format_exc()}'
                    logger.error(errmsg)
                    return {"errno": RET.TaskDBExportError, "errmsg": _("导出任务DB数据库失败"), "data": {}}
            except Exception:
                errmsg = f'导出任务DB数据库操作失败: {traceback.format_exc()}'
                logger.error(errmsg)
                return {"errno": RET.TaskDBOperationError, "errmsg": _("导出任务DB数据库操作失败"), "data": {}}

            return {"errno": RET.OK, "errmsg": _("成功"), "data": {"dst_name": task_ids, "dst_folder": dst_folder_path}}
        except Exception:
            errmsg = f'导出任务失败: {traceback.format_exc()}'
            logger.error(errmsg)
            return {"errno": RET.TaskExportFailure, "errmsg": "导出任务失败"}
