import re
from datetime import datetime
from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session, dynamic
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from . import group_crud, db_services, security, njwt

from models import user_models, db
from schemas import schemas

from utils import app_exeptions
from settings import security_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/ehouse/api/auth/users/token")


# def get_user_by_id(db: Session, username: str) -> user_models.User:
#     db_user = db.query(user_models.User).filter(user_models.User.id == username).first()
#     if not db_user:
#         raise app_exeptions.exception_not_found(
#             detail=f"User with username {username} not found"
#         )
#     return db_user


def check_password(password: str):
    if not re.search(security_settings.PASSWORD_TEMPLATE, password):
        raise app_exeptions.exception_password_not_match(
            detail="Password must contain at least eight characters. Password must contain letters and numbers. Password should not be too simple."
        )


def user_exist(db: Session, user: schemas.UserCteate):
    db_user_exist = (
        db.query(user_models.User)
        .filter(
            or_(
                user_models.User.username == user.username,
                user_models.User.email == user.email,
            )
        )
        .first()
    )
    if db_user_exist:
        raise app_exeptions.exception_duplicate(detail=f"user already exist")


def get_user(db: Session, username: str) -> user_models.User:
    db_user = (
        db.query(user_models.User).filter(user_models.User.username == username).first()
    )
    if not db_user:
        raise app_exeptions.exception_not_found(
            detail=f"User with username {username} not found"
        )
    return db_user


def delete_user(db: Session, username: str) -> user_models.User:
    db_user = get_user(username=username, db=db)
    db.delete(db_user)
    db_services.db_commit(db=db)
    return db_user


def get_user_list(
    db: Session, skip: int = 0, limit: int = 100
) -> List[user_models.User]:
    return db.query(user_models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCteate):
    user_exist(user=user, db=db)
    check_password(password=user.password)
    hashed_password = security.get_password_hash(user.password)
    db_user = user_models.User(
        username=user.username,
        comment=user.comment,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_root=user.is_root,
        hashed_password=hashed_password,
    )
    if user.group_name_list:
        groups = group_crud.get_grop_list_by_names(
            group_name_list=user.group_name_list, db=db
        )
        db_user.groups.extend(groups)
    db.add(db_user)
    db_services.db_commit(db=db)
    db.refresh(db_user)
    return db_user


def update_user(db: Session, username: str, user: schemas.UserUpdate):
    user_exist(user=user, db=db)
    db_user = get_user(db=db, username=username)
    db_user.username = user.username
    db_user.comment = user.comment
    db_user.email = user.email
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.is_active = user.is_active
    db_user.is_root = user.is_root

    if user.group_name_list != None:
        groups = group_crud.get_grop_list_by_names(
            group_name_list=user.group_name_list, db=db
        )
        db_user.groups.clear()
        db_user.groups.extend(groups)

    db.add(db_user)
    db_services.db_commit(db=db)
    db.refresh(db_user)
    return db_user


def change_password(db: Session, username: str, old_password: str, new_password: str):
    check_password(password=new_password)

    db_user = get_user(db=db, username=username)

    if security.verify_password(
        plain_password=old_password, hashed_password=db_user.hashed_password
    ):
        db_user.hashed_password = security.get_password_hash(password=new_password)
    else:
        raise app_exeptions.exception_unauthorized(detail="Password not correct")

    db.add(db_user)
    db_services.db_commit(db=db)
    db.refresh(db_user)
    return db_user


def reset_password(db: Session, username: str, new_password: str):
    check_password(password=new_password)
    db_user = get_user(db=db, username=username)
    db_user.hashed_password = security.get_password_hash(password=new_password)
    db.add(db_user)
    db_services.db_commit(db=db)
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user(username=username, db=db)
    if not security.verify_password(
        plain_password=password, hashed_password=db_user.hashed_password
    ):
        raise app_exeptions.exception_unauthorized(detail="Password is not correct")
    db_user.last_login_date = datetime.now()
    db.add(db_user)
    db_services.db_commit(db=db)
    db.refresh(db_user)
    return db_user


def get_current_user(
    db: Session = Depends(db.get_db), token: str = Depends(oauth2_scheme)
) -> user_models.User:

    jwt_data = njwt.get_data_from_token(token=token)
    if jwt_data.get("type") != "access":
        raise app_exeptions.exception_validate_jwt()
    db_user = get_user(db=db, username=jwt_data.get("sub"))
    return db_user


def get_refresh_user(db: Session, token: str) -> user_models.User:
    db_token = (
        db.query(user_models.RefreshTokenBlackList)
        .filter(user_models.RefreshTokenBlackList.refresh_token == token)
        .first()
    )
    if db_token:
        raise app_exeptions.exception_validate_jwt(detail="refresh token in black list")

    jwt_data = njwt.get_data_from_token(token=token)
    if jwt_data.get("type") != "refresh":
        raise app_exeptions.exception_validate_jwt()
    db_user = get_user(db=db, username=jwt_data.get("sub"))
    return db_user


def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> user_models.User:
    if current_user.is_active:
        return current_user
    raise app_exeptions.exception_inactive_user()


def create_tokens(username: str) -> schemas.Token:
    access_token = njwt.create_jwt_token(
        data={"sub": username},
        expires_delta=security_settings.EXPIRES_DELTA_ACCESS_TOKEN,
        token_type=security_settings.ACCESS_TOKEN_JWT_SUBJECT,
    )
    refresh_token = njwt.create_jwt_token(
        data={"sub": username},
        expires_delta=security_settings.EXPIRES_DELTA_REFRESH_TOKEN,
        token_type=security_settings.REFRESH_TOKEN_JWT_SUBJECT,
    )
    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=security_settings.TOKEN_TYPE,
    )


def has_permission(permission_name: str, user: user_models.User) -> None:
    if user.is_root:
        return
    if not user.has_permission(pemission_name=permission_name):
        raise app_exeptions.exception_forbidden()


def create_token_black_list(
    db: Session, refresh_token: str
) -> user_models.RefreshTokenBlackList:
    db_refresh_token = user_models.RefreshTokenBlackList(refresh_token=refresh_token)
    db.add(db_refresh_token)
    db_services.db_commit(db=db)
    db.refresh(db_refresh_token)
    return db_refresh_token
