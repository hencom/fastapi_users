from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas import schemas
from services import group_crud, users_crud, audit_crud, async_group_crud
from models import db

groups_router = APIRouter(
    prefix="/ehouse/api/auth/groups",
    tags=["Groups"],
)


@groups_router.get("/", response_model=List[schemas.BaseGroup])
def get_group_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_read_groups", user=user)
    groups = group_crud.get_group_list(db=db, skip=skip, limit=limit)
    return groups


@groups_router.post(
    "/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED
)
def create_group(
    group: schemas.GroupCreate,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_create_groups", user=user)
    db_group = group_crud.create_group(group=group, db=db)
    new_group = schemas.Group(
        id=db_group.id,
        name=db_group.name,
        comment=db_group.comment,
        permissions=db_group.permissions,
        users=db_group.users,
    )
    audit_crud.create_audit(
        table_name="groups",
        data_json=new_group.json(),
        history_type="insert",
        db=db,
        user=user,
    )
    return new_group


@groups_router.get("/{group_name}", response_model=schemas.Group)
def get_group(
    group_name: str,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_read_groups", user=user)
    db_group = group_crud.get_group(group_name=group_name, db=db)
    return schemas.Group(
        id=db_group.id,
        name=db_group.name,
        comment=db_group.comment,
        permissions=db_group.permissions,
        users=db_group.users,
    )


@groups_router.put("/{group_name}", response_model=schemas.Group)
def update_group(
    group_name: str,
    group: schemas.GroupCreate,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_update_groups", user=user)
    db_group = group_crud.update_group(group_name=group_name, group=group, db=db)
    new_group = schemas.Group(
        id=db_group.id,
        name=db_group.name,
        comment=db_group.comment,
        permissions=db_group.permissions,
        users=db_group.users,
    )
    audit_crud.create_audit(
        table_name="groups",
        data_json=new_group.json(),
        history_type="update",
        db=db,
        user=user,
    )
    return new_group


@groups_router.delete("/{group_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    group_name: str,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_delete_groups", user=user)
    db_group = group_crud.delete_group(group_name=group_name, db=db)
    new_group = schemas.Group(
        id=db_group.id,
        name=db_group.name,
        comment=db_group.comment,
        permissions=db_group.permissions,
        users=db_group.users,
    )
    audit_crud.create_audit(
        table_name="groups",
        data_json=new_group.json(),
        history_type="delete",
        db=db,
        user=user,
    )
    return new_group
