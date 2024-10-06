import datetime

from loguru import logger
from sqlalchemy import AsyncAdaptedQueuePool, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.settings.app import AppSettings

engine = create_engine(
    str(AppSettings.database_url), pool_size=20
)
SessionLocal = sessionmaker(bind=engine)

# Base = declarative_base()


# def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
#
#     logger.info("Connecting to PostgreSQL")
#
#     # 创建异步引擎,使用 asyncpg 驱动和连接池
#     async_engine = create_async_engine(
#         str(settings.database_url),
#         poolclass=AsyncAdaptedQueuePool,
#         pool_size=20,
#         max_overflow=0,
#         echo=True,
#     )
#
#     # 创建异步会话工厂
#     async_session_local = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
#
#     app.state.db = async_session_local
#
#     logger.info("Connection established")
#
#
# async def close_db_connection(app: FastAPI) -> None:
#     logger.info("Closing connection to database")
#
#     await app.state.db.close()
#
#     logger.info("Connection closed")

