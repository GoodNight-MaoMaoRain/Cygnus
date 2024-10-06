import logging
import random
import time
import json
import traceback
import zipfile
import datetime

from fastapi import Depends
from loguru import logger
from typing import Dict

from sqlalchemy.orm import Session

from app.common.response_code import RET
from app.db.pg_con import get_db
from app.lib.hardware.hardware.client import HttpClient
from fastapi.responses import JSONResponse
from app.schemas.schemas_engineer import LogFilterParams
from app.common.common import *
from fastapi_babel.core import _
from app.orm.models import SimulationData


# 管理和处理日志文件，包括列出日志文件、压缩日志文件、下载日志、筛选日志。
class LogsController:
    __instance = None

    @staticmethod
    def get_instance():
        if LogsController.__instance is None:
            LogsController.__instance = LogsController()
        return LogsController.__instance

    # 列出模块日志文件
    @staticmethod
    def list_log_files(db: Session = Depends(get_db)):
        try:
            # 组织各个模块日志,分别进行路径的拼接。
            python_logs_path = os.path.join(ROOT, "logs")
            product_logs_path = os.path.join(ROOT, "logs_user")
            go_logs_path = os.path.join(GO_ROOT, "error")

            # 确保路径存在
            if not os.path.exists(python_logs_path):
                raise FileNotFoundError(f"Python logs path not found: {python_logs_path}")
            if not os.path.exists(product_logs_path):
                raise FileNotFoundError(f"Product logs path not found: {product_logs_path}")
            if not os.path.exists(go_logs_path):
                raise FileNotFoundError(f"Go logs path not found: {go_logs_path}")

            # 打印路径下的文件
            try:
                logging.debug(f"Files in Python logs path: {os.listdir(python_logs_path)}")
            except Exception:
                errmsg = f'获取 Python 日志路径下文件失败: {str(traceback.format_exc())}'
                logging.error(errmsg)
                return {"errno": RET.GetPythonLogFilesFailed, "errmsg": _("获取 Python 日志路径下文件失败"), "data": {}}

            try:
                logging.debug(f"Files in Product logs path: {os.listdir(product_logs_path)}")
            except Exception:
                errmsg = f'获取 Product 日志路径下文件失败: {str(traceback.format_exc())}'
                logging.error(errmsg)
                return {"errno": RET.GetProductLogFilesFailed, "errmsg": _("获取 Product 日志路径下文件失败"),
                        "data": {}}

            try:
                logging.debug(f"Files in Go logs path: {os.listdir(go_logs_path)}")
            except Exception:
                errmsg = f'获取 Go 日志路径下文件失败: {str(traceback.format_exc())}'
                logging.error(errmsg)
                return {"errno": RET.GetGoLogFilesFailed, "errmsg": _("获取 Go 日志路径下文件失败"), "data": {}}

            try:
                python_log_file_list = [
                    {
                        "file_name": file_name,
                        "type": "python",
                        "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                            os.path.getmtime(os.path.join(python_logs_path, file_name))))
                    }
                    for file_name in os.listdir(python_logs_path)
                ]
            except Exception:
                errmsg = f'获取 Python 日志文件列表失败: {str(traceback.format_exc())}'
                logging.error(errmsg)
                python_log_file_list = []
                return {"errno": RET.GetPythonLogFileListFailed, "errmsg": _("获取 Python 日志文件列表失败"),
                        "data": {}}

            try:
                product_log_file_list = [
                    {
                        "file_name": file_name,
                        "type": "product",
                        "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                            os.path.getmtime(os.path.join(product_logs_path, file_name))))
                    }
                    for file_name in os.listdir(product_logs_path)
                ]
            except Exception:
                errmsg = f'获取 Product 日志文件列表失败: {str(traceback.format_exc())}'
                logging.error(errmsg)
                product_log_file_list = []
                return {"errno": RET.GetProductLogFileListFailed, "errmsg": _("获取 Product 日志文件列表失败"),
                        "data": {}}

            try:
                go_log_file_list = [
                    {
                        "file_name": file_name,
                        "type": "Go",
                        "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                            os.path.getmtime(os.path.join(go_logs_path, file_name))))
                    }
                    for file_name in os.listdir(go_logs_path)
                ]
            except Exception:
                errmsg = f'获取 Go 日志文件列表失败: {str(traceback.format_exc())}'
                logging.error(errmsg)
                go_log_file_list = []
                return {"errno": RET.GetGoLogFileListFailed, "errmsg": _("获取 Go 日志文件列表失败"), "data": {}}

            hardware_log_file_list = []
            fore_end_file_list = []

            python_log_file_list = [
                {"file_name": "default_python.log", "type": "python", "date": "2024-01-01 00:00:00"}
            ]

            product_log_file_list = [
                {"file_name": "default_product.log", "type": "product", "date": "2024-01-01 00:00:00"}
            ]

            go_log_file_list = [
                {"file_name": "default_go.log", "type": "Go", "date": "2024-01-01 00:00:00"}
            ]

            hardware_log_file_list = [
                {"file_name": "default_hardware.log", "type": "hardware", "date": "2024-01-01 00:00:00"}
            ]

            fore_end_file_list = [
                {"file_name": "default_fore_end.log", "type": "fore_end", "date": "2024-01-01 00:00:00"}
            ]

            log_modules = {
                "python": python_log_file_list,
                "product": product_log_file_list,
                "go": go_log_file_list,
                "hardware": hardware_log_file_list,
                "fore_end": fore_end_file_list,
            }

            # # 创建新记录并存储
            # new_simulation_data = SimulationData(log_modules=log_modules)
            # db.add(new_simulation_data)
            # db.commit()
            # db.refresh(new_simulation_data)  # 刷新以获取生成的 ID

            # 当你直接返回 log_modules 时，FastAPI 会自动将其转换为 JSON 格式，并且返回的数据结构与模型无关。因此，直接返回 log_modules 能正常工作。
            # return {"content": log_modules}
            return JSONResponse(content={"errno": RET.OK, "errmsg": "查看文件成功", "content": log_modules})
            # 使用 JSONResponse 可以显式地控制响应格式。content 会被正确地序列化为 JSON 格式，因此可以返回任意结构的数据。
        except Exception:
            errmsg = f'日志文件读取失败:{str(traceback.format_exc())}'
            logging.error(errmsg)
            return {"errno": RET.ReadLogFileFailed, "errmsg": "日志文件读取失败"}

    @staticmethod
    # 将指定目录下的所有文件压缩成一个 ZIP 文件，保持原有目录结构
    def zip_files(source_dir: str, output_file: str):
        try:
            logger.info(f"开始压缩目录: {source_dir} 到文件: {output_file}")
            # 创建一个新的 ZIP 文件
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # 计算相对路径，以保持原有目录结构
                        arcname = os.path.relpath(file_path, start=source_dir)
                        zipf.write(file_path, arcname=arcname)
                        logger.debug(f"已添加文件: {file_path} 为压缩包中的: {arcname}")

            logger.info(f"文件压缩完成: {output_file}")
            # 返回压缩文件的路径
            return output_file
        except Exception:
            errmsg = f'文件压缩失败: {str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.FileCompressFailed, "errmsg": "文件压缩失败"}

    # 选择对应的日志文件夹，格式化时间生成合法的文件名，调用 zip_files 进行压缩
    def download_logs(self, log_type: str) -> Dict:
        try:
            if not log_type:
                return {"errno": RET.LogModuleTypeError, 'errmsg': _("日志类型不能为空")}
            log_paths = {
                PYTHON_TYPE: PYTHON_LOG_PATH,
                GO_TYPE: GO_LOG_PATH,
                PRODUCT_TYPE: PRODUCT_LOG_PATH,
                HARDWARE_TYPE: HARDWARE_LOG_PATH
            }

            module_log_path = log_paths.get(log_type)
            if not module_log_path:
                errmsg = f"日志类型错误: {log_type}"
                logger.error(errmsg)
                return {"errno": RET.LogModuleTypeError, "errmsg": _("日志类型错误")}

            logger.info(f"开始下载日志类型: {log_type} 从路径: {module_log_path}")

            # 格式化时间以避免无效字符
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            zip_file_path = os.path.join(DOWNLOADS_PATH, f"{log_type}_{timestamp}_logs.zip")

            try:
                # 调用压缩方法
                logger.info(f"准备将日志压缩到: {zip_file_path}")
                zip_file_path = self.zip_files(module_log_path, zip_file_path)
            except Exception:
                errmsg = f"文件压缩错误: {str(traceback.format_exc())}"
                logger.error(errmsg)
                return {"errno": RET.FileCompressFailed, "errmsg": _("文件压缩错误"), "data": {}}

            if os.path.exists(zip_file_path):
                logger.info(f"日志文件成功压缩并保存到: {zip_file_path}")
                return {"errno": RET.OK, "errmsg": _("成功"), "data": {"log_path": zip_file_path}}
            else:
                errmsg = f"压缩文件不存在: {zip_file_path}"
                logger.error(errmsg)

                return {"errno": RET.FileDownloadFailed, "errmsg": _("文件下载错误"), "data": {}}

        except Exception:
            errmsg = f"日志下载失败: {str(traceback.format_exc())}"
            logger.error(errmsg)
            return {"errno": RET.FileCompressFailed, "errmsg": _("日志下载失败"), "data": {}}

    def filter_items(self, items, start_date, end_date, level, module_type):
        """
        按条件筛选
        :param items:
        :param start_date:
        :param end_date:
        :param level:
        :return:
        """
        filtered_items = []

        try:
            logger.info(
                f"开始筛选日志项，模块类型: {module_type}, 起始日期: {start_date}, 结束日期: {end_date}, 级别: {level}")

            # 将 start_date 和 end_date 转换为时间戳
            start_timestamp = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
            end_timestamp = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))

            if module_type == HARDWARE_TYPE:
                if level:
                    logger.info(f"筛选硬件日志，日志级别: {level}")
                    for item in items:
                        item_level = "WARN" if item.get("level").strip() == "WARNING" else item.get("level").strip()
                        if item_level == level:
                            filtered_items.append(item)
                else:
                    filtered_items = items
                    logger.info("硬件日志级别未指定，返回所有日志项")

            else:
                logger.info("筛选非硬件日志")

                for item in items:
                    try:
                        item_level = "WARN" if item.get("level").strip() == "WARNING" else item.get("level").strip()
                        date_str = item.get('time')
                        if all([start_date, end_date, level]):
                            if date_str:
                                _time_stamp = int(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S")))
                                if start_timestamp <= _time_stamp <= end_timestamp and item_level == level:
                                    filtered_items.append(item)
                        elif all([start_date, end_date]):
                            if date_str:
                                _time_stamp = int(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S")))
                                if start_timestamp <= _time_stamp <= end_timestamp:
                                    filtered_items.append(item)
                        elif level:
                            if item_level == level:
                                filtered_items.append(item)
                    except Exception:
                        errmsg = f"处理日志项时发生错误:{traceback.format_exc()}"
                        logger.error(errmsg)
                        continue

                logger.info(f"筛选完成，筛选后的日志项数: {len(filtered_items)}")
        except Exception:
            errmsg = f"日志筛选失败:{traceback.format_exc()}"
            logger.error(errmsg)

        return filtered_items

    # def filter_items(self, items, start_date, end_date, level, module_type):
    #     """
    #     按条件筛选
    #     :param items:
    #     :param start_date:
    #     :param end_date:
    #     :param level:
    #     :return:
    #     """
    #     filtered_items = []
    #     # 如果为硬件类型日志，若有不同日志级别返回则返回数据，否则返回按日期检索的全部数据
    #
    #     try:
    #         logger.info(
    #             f"开始筛选日志项，模块类型: {module_type}, 起始日期: {start_date}, 结束日期: {end_date}, 级别: {level}")
    #         if module_type == HARDWARE_TYPE:
    #             if level:
    #                 logger.info(f"筛选硬件日志，日志级别: {level}")
    #                 for item in items:
    #
    #                     item_level = "WARN" if item.get("level").strip() == "WARNING" else item.get("level").strip()
    #                     if item_level == level:
    #                         filtered_items.append(item)
    #             else:
    #                 filtered_items = items
    #                 logger.info("硬件日志级别未指定，返回所有日志项")
    #
    #         else:
    #             logger.info("筛选非硬件日志")
    #
    #             for item in items:
    #
    #                 try:
    #                     item_level = "WARN" if item.get("level").strip() == "WARNING" else item.get("level").strip()
    #                     date_str = item.get('time')
    #                     if all([start_date, end_date, level]):
    #                         if date_str:
    #
    #                             s_t = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    #                             _time_stamp = int(time.mktime(s_t))
    #                             if start_date <= _time_stamp <= end_date and item_level == level:
    #                                 filtered_items.append(item)
    #                     elif all([start_date, end_date]):
    #                         if date_str:
    #
    #                             s_t = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    #                             _time_stamp = int(time.mktime(s_t))
    #
    #                             if start_date <= _time_stamp <= end_date:
    #                                 filtered_items.append(item)
    #                     elif level:
    #                         if item_level == level:
    #                             filtered_items.append(item)
    #                 except Exception:
    #                     errmsg = f"处理日志项时发生错误:{traceback.format_exc()}"
    #                     logger.error(errmsg)
    #                     continue
    #             logger.info(f"筛选完成，筛选后的日志项数: {len(filtered_items)}")
    #     except Exception:
    #         errmsg = f"日志筛选失败:{traceback.format_exc()}"
    #         logger.error(errmsg)
    #
    #     return filtered_items

    # import time
    # 输入毫秒级的时间，转出正常格式的时间
    # @staticmethod
    # def _time_stamp(time_num):
    #     time_stamp = float(time_num / 1000)
    #     time_array = time.localtime(time_stamp)
    #     _time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    #
    #     _time = datetime.datetime.strptime(_time, "%Y-%m-%d %H:%M:%S")
    #     return _time
    ### 假数据
    def generate_fake_logs(self, num_logs=100):
        """
        生成假日志数据
        :param num_logs: 生成的日志条数
        :return: 日志列表
        """
        levels = ["INFO", "WARN", "ERROR", "DEBUG"]
        fake_logs = []
        fixed_paths = [
            "/home/user/project/file.py",
            "/usr/local/bin/app.go",
            "/var/log/system.log",
            "/etc/nginx/nginx.conf",
            "/opt/app/config.json"
        ]

        for _ in range(num_logs):
            log = {
                "time": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))).strftime(
                    "%Y-%m-%d %H:%M:%S"),
                "level": random.choice(levels),
                "message": f"这是一个模拟的日志消息 {_}",
                "module": random.choice(["PYTHON", "GO", "PRODUCT", "HARDWARE"]),
                "path": random.choice(fixed_paths)
            }
            fake_logs.append(log)

        return fake_logs

    def logs(self, params: LogFilterParams):
        start_date = None
        end_date = None
        try:
            if params.start_date and params.end_date:
                start_date = datetime.datetime.strptime(params.start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
                end_date = datetime.datetime.strptime(params.end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        except Exception:
            errmsg = f'时间信息格式错误: {str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.TimeFormatError, "errmsg": _("时间信息格式错误"), "data": {}}

        # 使用假数据进行测试
        all_log_list = self.generate_fake_logs(100)  # 生成100条假日志

        try:
            filter_log_list = self.filter_items(all_log_list, start_date, end_date, params.level, params.module_type)
            filter_log_list = sorted(filter_log_list, key=lambda l: l.get("time", 0))
        except Exception:
            errmsg = f'筛查日志信息失败:{str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.LogFilterFailed, "errmsg": _("筛查日志信息失败"), "data": {}}

        try:
            log_info_list = self.paginate(filter_log_list, params.page_limit, params.current_page)
        except Exception:
            errmsg = f'分页日志信息失败:{str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.LogPaginationError, "errmsg": _("分页日志信息失败"), "data": {}}

        data = {
            "total": len(filter_log_list),
            "current_page": params.current_page,
            "log_info_list": log_info_list
        }

        return {"errno": '0', "errmsg": _("成功"), "data": data}

    # def logs(self, params: LogFilterParams):
    #     start_date = None
    #     end_date = None
    #     try:
    #         if params.start_date and params.end_date:
    #             start_date = datetime.datetime.strptime(params.start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    #             end_date = datetime.datetime.strptime(params.end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    #             # start_date = int(datetime.datetime.strptime(params.start_date, '%Y-%m-%d').timestamp())
    #             # end_date = int(datetime.datetime.strptime(params.end_date, '%Y-%m-%d').timestamp())
    #     except Exception:
    #         errmsg = f'时间信息格式错误: {str(traceback.format_exc())}'
    #         logger.error(errmsg)
    #         return {"errno": RET.TimeFormatError, "errmsg": _("时间信息格式错误"), "data": {}}
    #
    #     if params.module_type == PYTHON_TYPE:
    #         module_log_path = PYTHON_LOG_PATH
    #     elif params.module_type == GO_TYPE:
    #         module_log_path = GO_LOG_PATH
    #     elif params.module_type == PRODUCT_TYPE:
    #         module_log_path = PRODUCT_LOG_PATH
    #     elif params.module_type == HARDWARE_TYPE:
    #         now_date = datetime.datetime.now().strftime("%Y-%m-%d")
    #         try:
    #             response_data = HttpClient.get_log()
    #             target_file_path = os.path.join(HARDWARE_LOG_PATH, f'{now_date}.log')
    #             with open(target_file_path, 'w', encoding="utf-8") as target_file:
    #                 target_file.write(response_data)
    #         except Exception:
    #             errmsg = f'保存硬件日志信息失败:{str(traceback.format_exc())}'
    #             logger.error(errmsg)
    #             return {"errno": RET.SaveHardwareLogFailed, "errmsg": _("保存硬件日志信息失败"), "data": {}}
    #     else:
    #         return {"errno": RET.InvalidModuleTypeError, "errmsg": _("无效的模块类型"), "data": {}}
    #
    #     try:
    #
    #         all_log_list = self.read_logs(params.module_type, start_date)
    #         if not isinstance(all_log_list, list):
    #             return {"errno": RET.ReadLogFileFailed, "errmsg": _("读取日志信息失败"), "data": {}}
    #
    #     except Exception:
    #         errmsg = f'读取日志信息失败:{str(traceback.format_exc())}'
    #         logger.error(errmsg)
    #         return {"errno": RET.ReadLogFileFailed, "errmsg": _("读取日志信息失败"), "data": {}}
    #
    #     try:
    #         filter_log_list = self.filter_items(all_log_list, start_date, end_date, params.level, params.module_type)
    #         filter_log_list = sorted(filter_log_list, key=lambda l: l.get("time", 0))
    #     except Exception:
    #         errmsg = f'筛查日志信息失败:{str(traceback.format_exc())}'
    #         logger.error(errmsg)
    #         return {"errno": RET.LogFilterFailed, "errmsg": _("筛查日志信息失败"), "data": {}}
    #
    #     try:
    #         log_info_list = self.paginate(filter_log_list, params.page_limit, params.current_page)
    #     except Exception:
    #         errmsg = f'分页日志信息失败:{str(traceback.format_exc())}'
    #         logger.error(errmsg)
    #         return {"errno": RET.LogPaginationError, "errmsg": _("分页日志信息失败"), "data": {}}
    #
    #     data = {
    #         "total": len(filter_log_list),
    #         "current_page": params.current_page,
    #         "log_info_list": log_info_list
    #     }
    #
    #     return {"errno": RET.OK, "errmsg": _("成功"), "data": data}

    def paginate(self, items, page_size, current_page):
        """
        分页
        :param items: 数据
        :param page_size: 每页条数
        :param current_page: 当前页
        :return:
        """
        start = (current_page - 1) * page_size
        end = start + page_size
        return items[start:end]

    # TODO 查看日志记录
    @staticmethod
    def read_logs(log_type, start_date):
        try:
            if log_type == PYTHON_TYPE:
                log_folder_path = os.path.join(PYTHON_LOG_PATH)
            elif log_type == GO_TYPE:
                log_folder_path = os.path.join(GO_LOG_PATH)
            elif log_type == PRODUCT_TYPE:
                log_folder_path = os.path.join(PRODUCT_LOG_PATH)
            elif log_type == HARDWARE_TYPE:
                log_folder_path = os.path.join(HARDWARE_LOG_PATH,
                                               '{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d")))
            else:
                errmsg = f'日志类型错误: {str(traceback.format_exc())}'
                logger.error(errmsg)
                return {"errno": RET.LogModuleTypeError, "errmsg": _("日志类型错误"), "data": {}}
        except Exception:
            errmsg = f'日志文件夹路径错误: {str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.LogFilePathError, "errmsg": _("日志文件夹路径错误"), "data": {}}

        log_list = []
        if log_type == HARDWARE_TYPE:
            try:
                with open(log_folder_path, 'r') as f:
                    log_lines = f.readlines()
                for log_line in log_lines:
                    try:
                        log_line_split = log_line.split(" ", 4)
                        _level = log_line_split[2]
                        _time = log_line_split[0] + " " + log_line_split[1]
                        _msg = log_line_split[4]
                        log_list.append({"time": _time, "level": _level, "message": _msg})
                    except Exception:
                        continue
            except Exception:
                errmsg = f"硬件日志信息查询失败: {str(traceback.format_exc())}"
                logger.error(errmsg)
        else:
            try:
                for file_name in os.listdir(log_folder_path):
                    log_path = os.path.join(log_folder_path, file_name)
                    if os.path.exists(log_path):
                        try:
                            with open(log_path, 'r', encoding='utf-8') as f:
                                log_lines = f.readlines()
                            for log_line in log_lines:
                                try:
                                    if "INFO:werkzeug" not in log_line:
                                        if log_type == PYTHON_TYPE:
                                            log_line_split = log_line.split(",")
                                            _level = log_line_split[2]
                                            _time = log_line_split[0]
                                            _msg = log_line_split[4]
                                        elif log_type == PRODUCT_TYPE:
                                            log_line_split = log_line.split(" ", 4)
                                            _level = log_line_split[2]
                                            _time = log_line_split[0] + " " + log_line_split[1]
                                            _msg = log_line_split[3] + " " + log_line_split[4]
                                        elif log_type == GO_TYPE:
                                            log_line = json.loads(log_line)
                                            _level = log_line.get("level").upper()
                                            _time = log_line.get("ts")
                                            _msg = log_line.get("msg")
                                        elif log_type == HARDWARE_TYPE:
                                            log_line = json.loads(log_line)
                                            _level = log_line.get("level").upper()
                                            _time = log_line.get("ts")
                                            _msg = log_line.get("msg")
                                        else:
                                            continue
                                        log_list.append({"time": _time, "level": _level, "message": _msg})
                                except Exception:
                                    continue
                        except Exception:
                            errmsg = f"日志文件读取失败: {traceback.format_exc()}"
                            logger.error(errmsg)
                            return {"errno": RET.ReadLogFileFailed, "errmsg": _("读取日志信息失败"), "data": {}}
            except Exception:
                errmsg = f"日志信息查询失败: {traceback.format_exc()}"
                logger.error(errmsg)
                return {"errno": RET.QueryLogInfoFailed, "errmsg": _("读取日志信息失败"), "data": {}}
        return log_list

    ### 假数据
    @staticmethod
    def get_log_data():
        # 假数据处理：这里可以根据实际情况从数据库或文件系统中提取
        return [
            {"level": " INFO", "message": "main.py:104|<module>: 运行服务器\n", "time": "2024-05-09 09:20:03"},
            {"level": " INFO", "message": "main.py:104|<module>: 运行服务器\n", "time": "2024-05-09 09:22:44"},
            {"level": " INFO", "message": "main.py:104|<module>: 运行服务器\n", "time": "2024-05-09 09:28:12"}
        ]

    def get_logs(self, log_type: str, level: str, page_limit: int, current_page: int) -> dict:
        log_data = self.get_log_data()

        # 假数据处理：这里可以根据实际情况从数据库或文件系统中提取
        filtered_logs = [log for log in log_data if level in log['level']]

        # 分页逻辑
        start = (current_page - 1) * page_limit
        end = start + page_limit
        paginated_logs = filtered_logs[start:end]

        response_data = {
            "current_page": current_page,
            "log_info_list": paginated_logs,
            "total": len(filtered_logs)
        }

        return response_data
