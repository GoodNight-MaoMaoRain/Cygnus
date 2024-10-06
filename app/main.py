from loguru import logger

from app.api.auth2.jwt import UserJwt
from app.middlewares.middleware_token import JWTAuthMiddleware

import pprint
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware
from fastapi_babel.middleware import BabelMiddleware

from app.core.settings.app import AppSettings
from app.core.config import get_app_settings
from app.db.pg_db import SessionLocal, engine
from app.orm.models import Base
from app.routers.api import router as api_router
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles


def get_application() -> FastAPI:
    # 获取系统配置
    settings = get_app_settings()

    # 配置日志信息
    settings.configure_logging()

    # 事件：创建表和关闭数据库连接
    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        # 创建表
        Base.metadata.create_all(bind=engine)
        yield
        # 关闭数据库连接
        engine.dispose()

    application = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)
    application.add_middleware(BabelMiddleware, babel_configs=AppSettings.babel_configs)

    if AppSettings.debug:
        logger.warning("程序为调试状态，未加载token验证")

    if not AppSettings.debug:
        application.add_middleware(JWTAuthMiddleware, verify_token=UserJwt.verify_token)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 中间件注入数据库连接
    @application.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = SessionLocal()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

    # 添加路由函数
    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = get_application()
# 挂载静态路由
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="CygnusS",
        # oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/swagger/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger/swagger-ui.css',
        swagger_favicon_url='/static/swagger/img.png',
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=get_app_settings().openapi_url,
        title=get_app_settings().title + " - ReDoc",
        redoc_js_url="/static/swagger/redoc.standalone.js",
    )


if __name__ == "__main__":
    # 打印路由
    pprint.pprint(app.routes)
    uvicorn.run(app, host="192.168.10.59", port=8007)
