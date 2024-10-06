import traceback
from sqlalchemy.orm import Session
from loguru import logger
from app.common.response_code import RET
from fastapi_babel.core import _
from app.crud.crud_setmarkhide import CrudSetMarkHide
from app.orm.models import SimulationData

class SetMarkHideController:
    __instance = None

    def __init__(self):
        self.crud = CrudSetMarkHide()

    @staticmethod
    def get_instance():
        if SetMarkHideController.__instance is None:
            SetMarkHideController.__instance = SetMarkHideController()
        return SetMarkHideController.__instance

    def set_mark_hide(self, db: Session, mark_file, mark_data, mark_id=1):
        try:
            logger.info(f'开始更新标记数据，mark_id: {mark_id}, mark_file: {mark_file}')

            # 更新数据库记录
            self.crud.update_setmark(db, mark_id, mark_file, mark_data)
            logger.info(f"标记数据更新成功，mark_id: {mark_id}")
            response = {"errno": RET.OK,
                        "errmsg": "OK",
                        "data": {}
            }


            new_simulation = SimulationData(
                set_mark_hide = response
            )
            db.add(new_simulation)
            db.commit()
            db.refresh(new_simulation)
            return response

        except Exception:
            db.rollback()  # 发生异常时回滚事务
            errmsg = f'更新标记数据失败:{str(traceback.format_exc())}'
            logger.error(errmsg)
            return {"errno": RET.DBUPDATEERR, "errmsg": _("更新标记数据失败"), "data": {}}
