from typing import List
from fastapi import HTTPException, status
import asyncpg
from utils import exeptions
from models import models
from schemas import groups as groups_schemas


async def get_group_list() -> List[models.Group]:
    return await models.Group.objects.select_related("permissions").all()


async def create_group(group: groups_schemas.GroupCreate) -> models.Group:
    try:
        db_permissionn_list = await models.Permission.objects.filter(
            name__in=group.permissions
        ).all()
        db_obj = await models.Group.objects.create(
            name=group.name, comment=group.comment
        )
        db_obj.permissions = db_permissionn_list
        await db_obj.update()
        return db_obj
    except asyncpg.exceptions.UniqueViolationError as ex:
        raise exeptions.exception_not_acceptable(detail=ex.as_dict())
