from typing import Any, AsyncIterator
from sqlalchemy import create_engine

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import databases

from settings.security_settings import SQLALCHEMY_DATABASE_URL

# SQLALCHEMY_DATABASE_URL = "postgresql://ehouseuser:ehouse2022@db_ehouse_users/dbusers"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,
)

# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# async_session = sessionmaker(async_engine, class_=AsyncSession)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# async def get_async_db() -> AsyncIterator[AsyncSession]:
#     async with async_session() as session:
#         yield session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy import event
