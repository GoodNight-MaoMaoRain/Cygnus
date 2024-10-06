import datetime
import traceback
from typing import Dict, Any

from fastapi_babel import _
from loguru import logger

from app.api.auth2.jwt import UserPasswd
from app.common.response_code import RET
from app.errors.errors import ErrorTemplate
from app.orm.models import User
from app.schemas.schemas_base import BaseResponseItem


class UserAuthGetDB:
    salt: str = ""
    hashed_password: str = ""

    def __init__(self):
        self.salt = UserPasswd().generate_salt()

    @staticmethod
    def get_users(db):
        # 检索用户是否存在
        users = db.query(User).all()
        return users

    @staticmethod
    def get_id_user(db, user_id: int):
        # 检索用户是否存在
        users = db.query(User).filter(User.id == user_id).first()
        return users

    @staticmethod
    def update_user_login_status(db, user_id: int) -> dict[str, str | Any]:

        ret = {"errno": RET.OK, "errmsg": "成功"}

        # 检索用户信息
        try:
            user_info = UserAuthGetDB().get_user_info(db)
        except Exception:
            errmsg = f"用户信息查询失败: {str(traceback.format_exc())}"
            logger.error(errmsg)
            ret.update({"errno": RET.QueryUserFailed, "errmsg": _("用户信息查询失败")})
            return ret

        # 查看本机是否有用户登录， 如果不是当前用户登录，则设置其他用户在线状态为False下线
        if user_info and user_info.id != user_id:

            is_login = False

            try:
                user_info.is_login = is_login
                db.commit()

            except Exception:
                errmsg = f"更改用户登录状态信息失败: {str(traceback.format_exc())}"
                logger.error(errmsg)
                ret.update({"errno": RET.ChangeUserLoginInfoFailed, "errmsg": _("更改用户登录状态信息失败")})
                return ret

        return ret

    def update_user_info(self, db, user_id: int, token: str, ip: str) -> dict[str, str | Any]:

        ret = {"errno": RET.OK, "errmsg": "成功"}

        # 检索用户信息
        try:
            user_info = self.get_id_user(db, user_id)
        except Exception:
            errmsg = f"用户信息查询失败: {str(traceback.format_exc())}"
            logger.error(errmsg)
            ret.update({"errno": RET.QueryUserFailed, "errmsg": _("用户信息查询失败")})
            return ret

        try:
            user_info.is_login = True
            user_info.token = token
            user_info.ip = ip
            db.commit()

        except Exception:
            errmsg = f"记录用户登录状态信息失败: {str(traceback.format_exc())}"
            logger.error(errmsg)
            ret.update({"errno": RET.RecordUserLoginInfoFailed, "errmsg": _("记录用户登录状态信息失败")})
            return ret

        return ret

    @staticmethod
    def get_login_user(db, user_name: str, is_deleted: bool):
        # 检索用户是否存在
        user = db.query(User).filter(User.user_name == user_name, User.deleted == is_deleted).first()
        return user

    def get_user_info(self, db):
        # 检索用户信息
        user_info = db.query.filter(*self.return_user_filter_condition()).first()
        return user_info

    def init_users(self, db) -> None:
        user = User()
        user.user_name = 'admin'
        user.password_hash = self.change_password("123456")
        user.createTime = datetime.datetime.now()
        user.role = 3
        db.add(user)

        user = User()
        user.user_name = 'operator'
        user.password_hash = self.change_password("123456")
        user.createTime = datetime.datetime.now()
        user.role = 1
        db.add(user)

        user = User()
        user.user_name = 'xiaoying'
        user.password_hash = self.change_password("123456")
        user.createTime = datetime.datetime.now()
        user.role = 0
        db.add(user)

        user = User()
        user.user_name = 'engineer'
        user.password_hash = self.change_password("123456")
        user.createTime = datetime.datetime.now()
        user.role = -1
        db.add(user)

        db.commit()

    def check_password(self, password: str, hashed_password: str) -> bool:
        return UserPasswd().verify_password(self.salt + password, hashed_password)

    def change_password(self, password: str) -> str:
        hashed_password = UserPasswd().get_password_hash(self.salt + password)
        return hashed_password

    @staticmethod
    def return_user_filter_condition():
        # 组织检索条件
        user_filter_condition = [User.deleted == False, User.role != "-1", User.is_login == True,
                                 User.ip == "192.168.100.1"]
        return user_filter_condition
