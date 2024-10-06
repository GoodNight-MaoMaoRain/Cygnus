import datetime
import traceback

from loguru import logger

from app.orm.models import Log


class LogsGetDB:

    # 记录操作日志信息
    @staticmethod
    def log_general(db, user, content, operation_type, log_type):

        try:
            log_info = Log()
            log_info.target = content
            log_info.operator = user.user_name
            log_info.operation_type = operation_type
            log_info.log_type = log_type
            log_info.create_time = datetime.datetime.now()
            db.add(log_info)
            db.commit()
        except Exception:
            db.rollback()
            errmsg = f"操作记录向pgsql提交失败:{str(traceback.format_exc())}"
            logger.error(errmsg)
