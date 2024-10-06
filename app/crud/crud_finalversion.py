from sqlalchemy.orm import Session
from app.orm.models import VersionInfo
from sqlalchemy import and_


class CrudFinalVersion:
    @staticmethod
    def get_final_version(session: Session):
        return session.query(VersionInfo).first()

    @staticmethod
    def get_version_by_name(session: Session, version_name: str):
        # 可以使用 SQLAlchemy 的 and_ 来确保条件始终有效
        return session.query(VersionInfo).filter(and_(VersionInfo.version_name == version_name)).first()
