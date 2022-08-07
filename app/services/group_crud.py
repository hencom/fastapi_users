from asyncio import exceptions
from typing import List
from sqlalchemy.orm import Session

from models import user_models
from schemas import schemas
from . import permissions_crud, db_services
from utils import app_exeptions


def get_group_by_id(db: Session, group_id: int) -> user_models.Group:
    db_group = (
        db.query(user_models.Group).filter(user_models.Group.id == group_id).first()
    )
    if not db_group:
        raise app_exeptions.exception_not_found(
            detail=f"Group with id {group_id} not found"
        )
    return db_group


def group_exist(db: Session, group: schemas.GroupCreate):
    db_exist_group = (
        db.query(user_models.Group).filter(user_models.Group.name == group.name).first()
    )
    if db_exist_group:
        raise app_exeptions.exception_duplicate(
            detail=f"group with name {group.name} already exist"
        )


def get_group(db: Session, group_name: str) -> user_models.Group:
    db_group = (
        db.query(user_models.Group).filter(user_models.Group.name == group_name).first()
    )
    if not db_group:
        raise app_exeptions.exception_not_found()
    return db_group


# def delete_group_with_id(db: Session, group_id: int) -> user_models.Group:
#     db_group = get_group_by_id(group_id=group_id, db=db)
#     db.delete(db_group)
#     db_services.db_commit(db=db)


def delete_group(db: Session, group_name: str) -> user_models.Group:
    db_group = get_group(group_name=group_name, db=db)
    db.delete(db_group)
    db_services.db_commit(db=db)
    return db_group


def get_group_list(
    db: Session, skip: int = 0, limit: int = 100
) -> List[user_models.Group]:
    db_group_list = db.query(user_models.Group).offset(skip).limit(limit).all()
    return db_group_list


def get_grop_list_by_names(
    db: Session, group_name_list: List[str]
) -> List[user_models.Group]:
    return (
        db.query(user_models.Group)
        .filter(user_models.Group.name.in_(group_name_list))
        .all()
    )


def create_group(db: Session, group: schemas.GroupCreate) -> user_models.Group:
    db_group = user_models.Group(name=group.name, comment=group.comment)
    group_exist(group=group, db=db)
    if group.permission_name_list:
        permissions = permissions_crud.get_permission_list_by_names(
            permission_name_list=group.permission_name_list, db=db
        )

        db_group.permissions.extend(permissions)
    db.add(db_group)
    # db_services.db_commit(db=db)
    db.commit()
    db.refresh(db_group)
    return db_group


# def update_group_with_id(
#     db: Session, group_id: int, group: schemas.GroupCreate
# ) -> user_models.Group:
#     db_group = get_group_by_id(db=db, group_id=group_id)
#     db_group.name = group.name
#     db_group.comment = group.comment
#     if group.permission != None:
#         permissions = permissions_crud.get_permission_list_by_names(
#             permission_name_list=group.permission, db=db
#         )
#         db_group.permissions.clear()
#         db_group.permissions.extend(permissions)
#     db.add(db_group)
#     db_services.db_commit(db=db)
#     db.refresh(db_group)
#     return db_group


def update_group(
    db: Session, group_name: str, group: schemas.GroupCreate
) -> user_models.Group:
    group_exist(group=group, db=db)
    db_group = get_group(db=db, group_name=group_name)
    db_group.name = group.name
    db_group.comment = group.comment

    db.add(db_group)

    if group.permission_name_list != None:
        permissions = permissions_crud.get_permission_list_by_names(
            permission_name_list=group.permission_name_list, db=db
        )

        db_group.permissions.clear()
        db_group.permissions.extend(permissions)
    db_services.db_commit(db=db)
    db.refresh(db_group)
    return db_group
