import sys
import getpass
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from models import db
from services import users_crud, permissions_crud
from schemas import schemas

_db = db.SessionLocal()


def ctreate_user(
    new_user: schemas.UserCteate,
    db: Session,
):
    db_user = users_crud.create_user(user=new_user, db=db)
    return schemas.UserDetail(
        username=db_user.username,
        id=db_user.id,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        is_active=db_user.is_active,
        is_root=db_user.is_root,
        last_login_date=db_user.last_login_date,
        joined_date=db_user.joined_date,
        comment=db_user.comment,
        groups=db_user.groups,
    )


def create_superuser():
    username = input("username: ")
    password = getpass.getpass("password: ")
    new_user = schemas.UserCteate(
        email=None,
        username=username,
        is_active=True,
        is_root=True,
        first_name=None,
        last_name=None,
        comment=None,
        password=password,
        group_name_list=None,
    )
    ctreate_user(new_user=new_user, db=_db)
    print("superuser successfully created")


def get_permission(permission_name: str, db: Session):
    db_permission = permissions_crud.get_permission(
        permission_name=permission_name, db=db
    )
    return db_permission


def create_permission(permission: schemas.PermissionCreate, db: Session):
    try:
        db_permission = get_permission(permission_name=permission.name, db=db)
        print(f"Permiision {permission.name} alreadi exist")
    except HTTPException as ex:
        print("------33-----", ex.status_code)
        if ex.status_code == 404:
            db_permission = permissions_crud.create_permission(
                permission=permission, db=db
            )
            print(f"Permiision {permission.name} created")

            return schemas.Permission(
                name=db_permission.name,
                comment=db_permission.comment,
                id=db_permission.id,
                groups=db_permission.groups,
            )


def create_all_permissions():
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_read_users", comment="can read users", group_name_list=None
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_create_users", comment="can create users", group_name_list=None
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_update_users", comment="can update users", group_name_list=None
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_delete_users", comment="can delete users", group_name_list=None
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_change_password",
            comment="can change password",
            group_name_list=None,
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_reset_password",
            comment="can reset password",
            group_name_list=None,
        ),
        db=_db,
    )

    # ===================

    create_permission(
        permission=schemas.PermissionCreate(
            name="can_read_permissions",
            comment="can read permissions",
            group_name_list=None,
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_create_permissions",
            comment="can create permissions",
            group_name_list=None,
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_update_permissions",
            comment="can update permissions",
            group_name_list=None,
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_delete_permissions",
            comment="can delete permissions",
            group_name_list=None,
        ),
        db=_db,
    )

    # ===================

    create_permission(
        permission=schemas.PermissionCreate(
            name="can_read_groups", comment="can read groups", group_name_list=None
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_create_groups", comment="can create groups", group_name_list=None
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_update_groups", comment="can update groups", group_name_list=None
        ),
        db=_db,
    )
    create_permission(
        permission=schemas.PermissionCreate(
            name="can_delete_groups", comment="can delete groups", group_name_list=None
        ),
        db=_db,
    )

    create_permission(
        permission=schemas.PermissionCreate(
            name="test_permission5!!!",
            comment="can delete groups",
            group_name_list=None,
        ),
        db=_db,
    )


if __name__ == "__main__":
    if sys.argv[1] == "createsuperuser":
        create_superuser()
    elif sys.argv[1] == "createpermissions":
        create_all_permissions()
