from typing import List
from sqlalchemy.orm import Session, dynamic
from . import db_services, group_crud

from models import user_models
from schemas import schemas

from utils import app_exeptions

# from sqlalchemy.orm.dynamic import AppenderQuery

# AppenderQuery.delete()


def get_permission(db: Session, permission_name: str) -> user_models.Permission:
    db_permission = (
        db.query(user_models.Permission)
        .filter(user_models.Permission.name == permission_name)
        .first()
    )
    if not db_permission:
        raise app_exeptions.exception_not_found(
            detail=f"Permission with name {permission_name} not found"
        )
    return db_permission


def delete_permission(db: Session, permission_name: str) -> user_models.Permission:
    db_permission = get_permission(permission_name=permission_name, db=db)
    db.delete(db_permission)
    db_services.db_commit(db=db)
    return db_permission


def get_permission_list(
    db: Session, skip: int = 0, limit: int = 100
) -> List[user_models.Permission]:
    return db.query(user_models.Permission).offset(skip).limit(limit).all()


def get_permission_list_by_names(
    db: Session, permission_name_list: List[str]
) -> List[user_models.Permission]:
    return (
        db.query(user_models.Permission)
        .filter(user_models.Permission.name.in_(permission_name_list))
        .all()
    )


def permission_exist(db: Session, permission: schemas.PermissionCreate) -> None:
    db_exist_permission = (
        db.query(user_models.Permission)
        .filter(user_models.Permission.name == permission.name)
        .first()
    )
    if db_exist_permission:
        raise app_exeptions.exception_duplicate(
            detail=f"group wiht name {permission.name} already exist"
        )


def create_permission(
    db: Session, permission: schemas.PermissionCreate
) -> user_models.Permission:
    permission_exist(permission=permission, db=db)
    db_permission = user_models.Permission(
        name=permission.name, comment=permission.comment
    )
    if permission.group_name_list:
        groups = group_crud.get_grop_list_by_names(
            group_name_list=permission.group_name_list, db=db
        )

        db_permission.groups.extend(groups)
    db.add(db_permission)
    db_services.db_commit(db=db)
    db.refresh(db_permission)
    return db_permission


def update_permission(
    db: Session, permission_name: str, permission: schemas.PermissionCreate
) -> user_models.Permission:
    permission_exist(permission=permission, db=db)
    db_permission = get_permission(permission_name=permission_name, db=db)
    db_permission.name = permission.name
    db_permission.comment = permission.comment

    if permission.group_name_list != None:
        groups = group_crud.get_grop_list_by_names(
            group_name_list=permission.group_name_list, db=db
        )
        db_permission.groups.clear()
        db_permission.groups.extend(groups)
    db.add(db_permission)
    db_services.db_commit(db=db)
    db.refresh(db_permission)
    return db_permission
