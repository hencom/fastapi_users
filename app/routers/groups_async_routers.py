from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import schemas
from services import group_crud, users_crud, audit_crud, async_group_crud
from models import db

groups_router = APIRouter(
    prefix="/ehouse/api/auth/async/groups",
    tags=["Async Groups"],
)


@groups_router.get("/", response_model=List[schemas.BaseGroup])
async def async_get_group_list(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(db.get_async_db)
):
    return await async_group_crud.get_group_list(db=db, limit=limit, offset=offset)


@groups_router.get("/{group_name}")
async def async_get_group(group_name: str, db: AsyncSession = Depends(db.get_async_db)):
    res = await async_group_crud.get_group(db=db, group_name=group_name)
    return schemas.Group(**res.__dict__)


@groups_router.post("/", response_model=schemas.Group)
async def create_group(
    group: schemas.GroupCreate, db: AsyncSession = Depends(db.get_async_db)
):
    res = await async_group_crud.create_group(db=db, group=group)
    return res
