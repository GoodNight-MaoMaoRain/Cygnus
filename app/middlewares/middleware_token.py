# 自定义中间件类
import os
from typing import Callable

import jwt
from fastapi import FastAPI, Request
from fastapi_babel import _
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.common.response_code import RET


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, verify_token: Callable[[str], bool]):
        super().__init__(app)
        self.verify_token = verify_token

    async def dispatch(self, request: Request, call_next: Callable):
        # 从请求头中获取 Authorization 字段
        auth_header = request.headers.get("Authorization")
        accept_language = request.headers.get("Accept-Language")

        if "zh" in accept_language:
            accept_language = "zh"

        if auth_header:
            try:
                # 从 Authorization 字段获取 token
                token = auth_header.split(" ")[1]
                # 验证 token
                user_info = self.verify_token(token)
                if user_info:
                    # 将用户信息存储在 Request 对象的 state 属性中
                    request.state.user = user_info
                    return await call_next(request)

                else:
                    # 如果 token 验证失败
                    errmsg = '权限校验失败 'if accept_language == "zh" else 'Permission verification failed'
                    logger.error(errmsg)
                    return JSONResponse({"errno": RET.PrivilegeVerifiedFailed, "errmsg": errmsg})
            except (IndexError, jwt.exceptions.DecodeError):
                # 如果 Authorization 字段格式不正确或 token 解码失败,返回 401 Unauthorized 响应
                errmsg = '权限校验失败 'if accept_language == "zh" else 'Permission verification failed'
                logger.error(errmsg)
                return JSONResponse({"errno": RET.PrivilegeVerifiedFailed, "errmsg": _('权限校验失败')})
        else:
            # 如果请求头中没有 Authorization 字段,返回 401 Unauthorized 响应
            errmsg = 'token缺失 ' if accept_language == "zh" else 'token missing'
            logger.error(errmsg)
            return JSONResponse({"errno": RET.MISSTOKEN, "errmsg": errmsg})
