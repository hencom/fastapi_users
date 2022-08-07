from datetime import datetime
from typing import List, Optional, Text
from pydantic import EmailStr
from pydantic.main import BaseModel


class BasePermissionsGroups(BaseModel):
    name: str
    comment: Optional[Text] = None


class GroupCreate(BasePermissionsGroups):
    permission_name_list: Optional[List[str]] = None
    # username_list: Optional[List[str]] = None


class PermissionCreate(BasePermissionsGroups):
    group_name_list: Optional[List[str]] = None


class BasePermission(BasePermissionsGroups):
    id: int

    class Config:
        orm_mode = True


class BaseGroup(BasePermissionsGroups):
    id: int

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    email: Optional[EmailStr] = None
    username: str
    is_active: bool = True
    is_root: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    comment: Optional[Text] = None

    class Config:
        orm_mode = True


class Permission(BasePermission):
    groups: List[BaseGroup] = []

    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    joined_date: datetime
    last_login_date: datetime = None

    class Config:
        orm_mode = True


class UserDetail(User):
    groups: List[BaseGroup] = []
    permissions: List[BasePermission] = []

    class Config:
        orm_mode = True


class Group(BaseGroup):
    permissions: List[BasePermission] = []
    users: List[User] = []

    class Config:
        orm_mode = True


class UserInDb(UserDetail):
    hashed_password: str

    class Config:
        orm_mode = True


class UserCteate(BaseUser):
    password: str
    group_name_list: Optional[List[str]] = None


class UserUpdate(BaseUser):
    group_name_list: Optional[List[str]] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str
