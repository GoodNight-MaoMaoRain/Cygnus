import datetime
from typing import Callable
from fastapi import Request, FastAPI
from loguru import logger
from app.core.settings.app import AppSettings
# from app.db.pg_db import connect_to_db, close_db_connection


# def create_start_app_handler(
#     app: FastAPI,
#     settings: AppSettings,
# ) -> Callable:  # type: ignore
#     def start_app() -> None:
#         connect_to_db(app, settings)
#
#     return start_app
#
#
# def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
#     @logger.catch
#     async def stop_app() -> None:
#         await close_db_connection(app)
#
#     return stop_app


# def create_init_user_handler(
#     app: FastAPI,
#     settings: AppSettings,
# ):
#     print(app.state.db, "create_init_user_handler")

