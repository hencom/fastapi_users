from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models import user_models

from models import db
from schemas import schemas
from services import permissions_crud, users_crud, audit_crud

permissions_router = APIRouter(
    prefix="/ehouse/api/auth/permissions",
    tags=["Permissions"],
)


@permissions_router.get("/", response_model=List[schemas.BasePermission])
def get_permission_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_read_permissions", user=user)
    permissions = permissions_crud.get_permission_list(db=db, skip=skip, limit=limit)
    return permissions


@permissions_router.post(
    "/", response_model=schemas.Permission, status_code=status.HTTP_201_CREATED
)
def create_permission(
    permission: schemas.PermissionCreate,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_create_permissions", user=user)
    db_permission = permissions_crud.create_permission(permission=permission, db=db)
    new_permission = schemas.Permission(
        name=db_permission.name,
        comment=db_permission.comment,
        id=db_permission.id,
        groups=db_permission.groups,
    )
    audit_crud.create_audit(
        table_name="permissions",
        data_json=new_permission.json(),
        history_type="insert",
        db=db,
        user=user,
    )
    return new_permission


@permissions_router.get("/{permission_name}", response_model=schemas.Permission)
def get_permission(
    permission_name: str,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_read_permissions", user=user)
    db_permission = permissions_crud.get_permission(
        permission_name=permission_name, db=db
    )
    return schemas.Permission(
        name=db_permission.name,
        comment=db_permission.comment,
        id=db_permission.id,
        groups=db_permission.groups,
    )


@permissions_router.put("/{permission_name}", response_model=schemas.Permission)
def update_permission(
    permission_name: str,
    permission: schemas.PermissionCreate,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_update_permissions", user=user)
    db_permission = permissions_crud.update_permission(
        permission_name=permission_name, permission=permission, db=db
    )
    new_permission = schemas.Permission(
        name=db_permission.name,
        comment=db_permission.comment,
        id=db_permission.id,
        groups=db_permission.groups,
    )
    audit_crud.create_audit(
        table_name="permissions",
        data_json=new_permission.json(),
        history_type="update",
        db=db,
        user=user,
    )
    return new_permission


@permissions_router.delete("/{permission_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_name: str,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
) -> None:
    users_crud.has_permission("can_delete_permissions", user=user)
    db_permission = permissions_crud.delete_permission(
        permission_name=permission_name, db=db
    )
    new_permission = schemas.Permission(
        name=db_permission.name,
        comment=db_permission.comment,
        id=db_permission.id,
        groups=db_permission.groups,
    )
    audit_crud.create_audit(
        table_name="permissions",
        data_json=new_permission.json(),
        history_type="delete",
        db=db,
        user=user,
    )
    return new_permission
