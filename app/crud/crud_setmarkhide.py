from sqlalchemy.orm import Session
from app.orm.models import Mark
from sqlalchemy import and_


class CrudSetMarkHide:

    def __init__(self):
        pass

    def update_setmark(self, session: Session, mark_id: int, mark_file: bool, mark_data: bool):
        session.query(Mark).filter_by(id=mark_id).update({
            "mark_data": mark_data,
            "mark_file": mark_file
        })
        session.commit()
        return True
