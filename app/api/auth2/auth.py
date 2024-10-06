import traceback
from datetime import timedelta
from http.client import HTTPException
from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.openapi.models import Response
from fastapi_babel.core import _
from loguru import logger
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.api.auth2.jwt import UserJwt, create_access_token
from app.api.engineer.dynamic_routing import authenticate_user, get_routes_based_on_role
from app.common.common import LOG_OPERATION
from app.common.response_code import RET
from app.crud.crud_auth import UserAuthGetDB
from app.crud.crud_logs import LogsGetDB
from app.db.pg_con import get_db
from app.orm.models import UserRole
from app.schemas.schemas_user import BaseResponseItem, LoginRequestItem, LoginResponseItem, LoginRequest, \
    CreateUserRequest
from app.core.settings.app import AppSettings

router = APIRouter()


@router.get("/init_users", name="users:init_users", response_model=BaseResponseItem)
async def init_users(db: Session = Depends(get_db)) -> Any:
    # 查询是否已初始化用户数据
    try:
        exist_users = UserAuthGetDB().get_users(db)

    except Exception:
        errmsg = f"查询用户信息失败: {str(traceback.format_exc())}"
        logger.error(errmsg)
        return {"errno": RET.DBQUERYERR, "errmsg": _('查询用户信息失败')}

    # 若不存在则创建
    if not exist_users:

        try:
            # 创建用户
            UserAuthGetDB().init_users(db)
        except Exception:
            errmsg = f"初始化用户信息失败: {str(traceback.format_exc())}"
            logger.error(errmsg)
        return {"errno": RET.DBQUERYERR, "errmsg": _('查询用户信息失败')}

    return {"errno": RET.OK, "errmsg": _('成功')}



# @router.post("/create_user")
# def create_user_endpoint(request: CreateUserRequest, db: Session = Depends(get_db)):
#     user = db.query(UserRole).filter(UserRole.username == request.user_name).first()
#
#     # 检查用户名是否已存在
#     if user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#
#     # 创建用户并返回成功响应
#     new_user = create_user(db, request.user_name, request.password)
#     return {"errno": "0", "errmsg": "用户创建成功", "data": {"user_name": new_user.username}}


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """登录接口"""
    try:
        # 认证用户
        user = authenticate_user(db, request.user_name, request.password_hash)

        # 生成 JWT token
        access_token_expires = timedelta(minutes=3000)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role_id},
            expires_delta=access_token_expires
        )

        header = {
            "token": access_token
        }

        if user.username == 'engineer':
            permission = 'engineer'
        elif user.username == 'superengineer':
            permission = 'superengineer'


        return JSONResponse(
            headers=header,
            content = {
            "errno": "0",
            "errmsg": "成功",
            "data": {
                "role": str(user.role_id),
                "user_name": user.username,
                "token": access_token,
                "permissions":[f"permission:{permission}"]
            }
        })
    except HTTPException as e:
        raise e

    except Exception:
        return {
            "errno": "1",
            "errmsg": "登陆失败，请输入正确的用户名或密码"
        }

# @router.post("/login")
# def login(request: LoginRequest, db: Session = Depends(get_db)):
#     """登录接口"""
#     try:
#         user = authenticate_user(db, request.user_name, request.password_hash)
#         return get_routes_based_on_role(user)
#     except Exception:
#         return {"errno": "1", "errmsg": "登陆失败，请输入正确的用户名或密码"}

    # ip = request.client.host
    # user_name = item.user_name
    # password = item.password_hash
    #
    # # 校验用户名和密码
    # if not all([user_name, password]):
    #     errmsg = f"参数不完整: {str([user_name])}"
    #     logger.warning(errmsg)
    #     return {"errno": RET.MISSPAR, "errmsg": _("参数不完整")}
    #
    # # 查询该用户是否存在
    # try:
    #     user = UserAuthGetDB().get_login_user(db, user_name, False)
    # except Exception:
    #     errmsg = f"登录失败，输入用户名为{user_name}: {str(traceback.format_exc())}"
    #     logger.error(errmsg)
    #     return {"errno": RET.DBQUERYERR, "errmsg": _("登录失败，请重试")}
    #
    # if user is None:
    #     logger.warning("请输入正确的账号密码")
    #     return {"errno": RET.EnterCorrectAccountPasswd, "errmsg": _("请输入正确的账号密码")}
    #
    # # 生成token
    # try:
    #     token = UserJwt().create_access_token_for_user(user.id, user_name, AppSettings.secret_key)
    # except Exception:
    #     errmsg = f"生成token失败，输入信息为:{user.id, user_name, AppSettings.secret_key}: {str(traceback.format_exc())}"
    #     logger.error(errmsg)
    #     return {"errno": RET.UserLoginERR, "errmsg": _("用户登录失败")}
    #
    # # 校验密码
    # if UserAuthGetDB().check_password(password, user.password_hash):
    #
    #     data = {
    #         "role": user.role,
    #         "user_name": user_name,
    #         "token": token,
    #     }
    #
    #     # request.state.user = user
    #     #
    #     # try:
    #     #
    #     #     # 更新用户登录状态
    #     #     ret = UserAuthGetDB().update_user_login_status(db, user.id)
    #     #
    #     #     # 有错误则返回错误信息
    #     #     if ret.get("errno") != RET.OK:
    #     #         return {}.update(ret)
    #     #
    #     # except Exception:
    #     #     errmsg = f"用户信息查询失败:{str(traceback.format_exc())}"
    #     #     logger.error(errmsg)
    #     #     return {"errno": RET.ChangeUserLoginInfoFailed, "errmsg": _("更改用户登录状态信息失败")}
    #     #
    #     # try:
    #     #
    #     #     # 数据库中更新用户信息
    #     #     ret = UserAuthGetDB().update_user_info(db, user.id, token, ip)
    #     #
    #     #     # 有错误则返回错误信息
    #     #     if ret.get("errno") != RET.OK:
    #     #         return {}.update(ret)
    #     #
    #     # except Exception:
    #     #
    #     #     errmsg = f"记录用户登录状态信息失败:{str(traceback.format_exc())}"
    #     #     logger.error(errmsg)
    #     #     return {"errno": RET.RecordUserLoginInfoFailed, "errmsg": _("记录用户登录状态信息失败")}
    #     #
    #     # # 操作记录
    #     # LogsGetDB().log_general(db, user, "登录软件", "信息", LOG_OPERATION)
    #
    #     return {"errno": RET.OK, "errmsg": _("成功"), "data": data}

    # else:
    #     logger.warning("账号或密码错误")
    #     return {"errno": RET.PleaseCorrectUsernameOrPasswd, "errmsg": _("请输入正确的账号密码")}
