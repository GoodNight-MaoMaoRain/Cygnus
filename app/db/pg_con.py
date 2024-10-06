from typing import AsyncGenerator, Type, Callable
from fastapi import Request, Depends
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.pg_db import SessionLocal


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_db(request: Request):
#     return request.state.db

# def _get_db_pool(request: Request):
#
#     with request.app.state.db() as db:
#         return db

# def _get_connection_from_pool(
#         db: async_sessionmaker = Depends(_get_db_pool),
# ):
#     async with db() as db:
#         yield db


# def get_repository(
#         repo_type: Type[BaseRepository],
# ) -> Callable[[Connection], BaseRepository]:
#     def _get_repo(
#             conn: Connection = Depends(_get_connection_from_pool),
#     ) -> BaseRepository:
#         return repo_type(conn)
#
#     return _get_repo
