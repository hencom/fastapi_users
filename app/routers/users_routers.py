from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import user_models
from services import users_crud, audit_crud
from models import db
from schemas import schemas
from utils import app_exeptions

from settings import security_settings


users_router = APIRouter(
    prefix="/ehouse/api/auth/users",
    tags=["Users"],
)


@users_router.get(
    "/",
    response_model=List[schemas.User],
    description="permission: can_read_users",
    status_code=status.HTTP_200_OK,
)
def get_user_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db),
    user: user_models.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_read_users", user=user)
    users = users_crud.get_user_list(db=db, skip=skip, limit=limit)
    return users


@users_router.post(
    "/",
    response_model=schemas.UserDetail,
    description="permission: can_create_users",
    status_code=status.HTTP_201_CREATED,
)
def ctreate_user(
    new_user: schemas.UserCteate,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_create_users", user=user)
    db_user = users_crud.create_user(user=new_user, db=db)
    sch_user = schemas.UserDetail(
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
    audit_crud.create_audit(
        table_name="users",
        data_json=sch_user.json(),
        history_type="insert",
        db=db,
        user=user,
    )
    return sch_user


@users_router.get(
    "/me", response_model=schemas.UserDetail, status_code=status.HTTP_200_OK
)
def get_current_user(
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    return schemas.UserDetail(
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_root=user.is_root,
        first_name=user.first_name,
        last_name=user.last_name,
        comment=user.comment,
        id=user.id,
        joined_date=user.joined_date,
        last_login_date=user.last_login_date,
        groups=user.groups,
        permissions=user.permissions,
    )


@users_router.post(
    "/me/change-password",
    response_model=schemas.User,
    status_code=status.HTTP_202_ACCEPTED,
)
def change_password_for_current_user(
    old_password: str,
    new_password: str,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    db_user = users_crud.change_password(
        username=user.username,
        old_password=old_password,
        new_password=new_password,
        db=db,
    )
    sch_user = schemas.UserDetail(
        email=db_user.email,
        username=db_user.username,
        is_active=db_user.is_active,
        is_root=db_user.is_root,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        comment=db_user.comment,
        id=db_user.id,
        joined_date=db_user.joined_date,
        last_login_date=db_user.last_login_date,
        groups=db_user.groups,
    )
    audit_crud.create_audit(
        table_name="users",
        data_json=sch_user.json(),
        history_type="change_password",
        db=db,
        user=user,
    )
    return sch_user


@users_router.get(
    "/{username}",
    response_model=schemas.UserDetail,
    description="permission: can_read_users",
    status_code=status.HTTP_200_OK,
)
def get_user(
    username: str,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_read_users", user=user)
    db_user = users_crud.get_user(username=username, db=db)
    return schemas.UserDetail(
        email=db_user.email,
        username=db_user.username,
        is_active=db_user.is_active,
        is_root=db_user.is_root,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        comment=db_user.comment,
        id=db_user.id,
        joined_date=db_user.joined_date,
        last_login_date=db_user.last_login_date,
        groups=db_user.groups,
    )


@users_router.post(
    "/{username}/reset-password",
    response_model=schemas.UserDetail,
    description="permission: can_change_password",
    status_code=status.HTTP_202_ACCEPTED,
)
def reset_password(
    username: str,
    new_password: str,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_change_password", user=user)
    db_user = users_crud.reset_password(
        username=username, new_password=new_password, db=db
    )
    sch_user = schemas.UserDetail(
        email=db_user.email,
        username=db_user.username,
        is_active=db_user.is_active,
        is_root=db_user.is_root,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        comment=db_user.comment,
        id=db_user.id,
        joined_date=db_user.joined_date,
        last_login_date=db_user.last_login_date,
        groups=db_user.groups,
    )
    audit_crud.create_audit(
        table_name="users",
        data_json=sch_user.json(),
        history_type="reset_password",
        db=db,
        user=user,
    )
    return sch_user


@users_router.put(
    "/{username}",
    response_model=schemas.UserDetail,
    description="permission: can_update_users",
    status_code=status.HTTP_200_OK,
)
def update_user(
    username: str,
    update_user: schemas.UserUpdate,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_update_users", user=user)
    db_user = users_crud.update_user(username=username, user=update_user, db=db)
    sch_user = schemas.UserDetail(
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
    audit_crud.create_audit(
        table_name="users",
        data_json=sch_user.json(),
        history_type="update",
        db=db,
        user=user,
    )
    return sch_user


@users_router.delete(
    "/{username}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="permission: can_delete_users",
)
def delete_user(
    username: str,
    db: Session = Depends(db.get_db),
    user: schemas.User = Depends(users_crud.get_current_active_user),
):
    users_crud.has_permission("can_delete_users", user=user)
    db_user = users_crud.delete_user(username=username, db=db)
    sch_user = schemas.UserDetail(
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
    audit_crud.create_audit(
        table_name="users",
        data_json=sch_user.json(),
        history_type="delete",
        db=db,
        user=user,
    )
    return sch_user


@users_router.post(
    "/token", response_model=schemas.Token, status_code=status.HTTP_200_OK
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)
):
    db_user = users_crud.authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    return users_crud.create_tokens(username=db_user.username)


@users_router.post(
    "/refresh", response_model=schemas.Token, status_code=status.HTTP_200_OK
)
def refresh_token(
    token: schemas.RefreshToken,
    db: Session = Depends(db.get_db),
):
    db_user = users_crud.get_refresh_user(token=token.refresh_token, db=db)
    users_crud.create_token_black_list(refresh_token=token.refresh_token, db=db)
    return users_crud.create_tokens(username=db_user.username)
