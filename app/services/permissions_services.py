from typing import List
from fastapi import HTTPException, status
import asyncpg
from utils import exeptions
from models import models
from schemas import permissions as permission_schemas


async def get_permissions() -> List[models.Permission]:
    return await models.Permission.objects.all()


async def create_permission(permission: permission_schemas.PermissionCreate):
    db_permission = models.Permission(name=permission.name, comment=permission.comment)
    try:
        await db_permission.save()
    except asyncpg.exceptions.UniqueViolationError as ex:
        raise exeptions.exception_not_acceptable(detail=ex.as_dict())

    # for group_name in permission.groups:
    #     db_group = await models.Group.objects.get_or_none(name=group_name)
    #     if db_group:
    #         await db_permission.groups.add(db_group)
    return db_permission


async def get_permission(name: str) -> models.Permission:
    db_permission = await models.Permission.objects.get_or_none(name=name)
    if not db_permission:
        raise exeptions.exception_not_found()
    return db_permission


async def update_permission(
    name: str, permission: permission_schemas.PermissionCreate
) -> models.Permission:
    db_permission = await models.Permission.objects.get_or_none(name=name)
    if not db_permission:
        raise exeptions.exception_not_found()
    db_permission.name = permission.name
    db_permission.comment = permission.comment
    try:
        await db_permission.update()
    except asyncpg.exceptions.UniqueViolationError as ex:
        raise exeptions.exception_not_acceptable(detail=ex.as_dict())
    return db_permission


async def delete_permission(name: str) -> None:
    db_permission = await models.Permission.objects.get_or_none(name=name)
    if not db_permission:
        raise exeptions.exception_not_found()
    await db_permission.delete()
