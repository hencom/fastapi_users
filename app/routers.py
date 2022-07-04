from typing import List
from fastapi import APIRouter, status

from services import services, permissions_services, groups_services
from models import models
from schemas import users as users_schemas
from schemas import permissions as permission_schemas
from schemas import groups as groups_schemas

users_router = APIRouter(
    prefix="/ehouse/api/users",
    tags=["Users"],
)


@users_router.get("/{username}", response_model=models.User)
async def get_user(username: str):
    return await services.get_user(username=username)


@users_router.put("/{username}", response_model=models.User)
async def update_user(username: str, user: models.User):
    return await services.get_user(username=username)


@users_router.delete("/{username}", response_model=models.User)
async def update_user(username: str):
    return await services.get_user(username=username)


@users_router.post("/", response_model=models.User)
async def create_user(user: users_schemas.UserCreate):
    return await services.create_user(user=user)


groups_router = APIRouter(
    prefix="/ehouse/api/users/groups",
    tags=["Groups"],
)


@groups_router.get("/", response_model=List[models.Group])
async def get_group_list():
    return await groups_services.get_group_list()


@groups_router.post("/", response_model=models.Group)
async def create_group(group: groups_schemas.GroupCreate):
    return await groups_services.create_group(group=group)


permissions_router = APIRouter(
    prefix="/ehouse/api/users/permissions",
    tags=["Permissions"],
)


@permissions_router.get("/", response_model=List[models.Permission])
async def get_permission_list():
    return await permissions_services.get_permissions()


@permissions_router.post("/", response_model=models.Permission)
async def create_permission(
    permission: models.Permission.get_pydantic(exclude={"id"}),
):
    return await permissions_services.create_permission(permission=permission)


@permissions_router.get("/{name}", response_model=models.Permission)
async def get_permission(name: str):
    return await permissions_services.get_permission(name=name)


@permissions_router.put("/{name}", response_model=models.Permission)
async def update_permission(
    name: str,
    permission: permission_schemas.PermissionCreate,
):
    return await permissions_services.update_permission(
        name=name, permission=permission
    )


@permissions_router.delete(
    "/{name}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_permission(name: str):
    return await permissions_services.delete_permission(name=name)
