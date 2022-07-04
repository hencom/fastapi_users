import datetime
import typing
import typing
from email.policy import default
from enum import unique
import databases
import sqlalchemy
import pydantic

import ormar

DB_URL = "postgresql://ehouseuser:ehouse2022@db_ehouse_users/dbusers"

engine = sqlalchemy.create_engine(DB_URL)


database = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta:
    database = database
    metadata = metadata


class Permission(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "permissions"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50, unique=True)
    comment: typing.Optional[typing.Text] = ormar.Text(default=None, nullable=True)


class Group(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "groups"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50, unique=True)
    comment: typing.Optional[typing.Text] = ormar.Text(default=None, nullable=True)
    permissions: typing.Optional[typing.List[Permission]] = ormar.ManyToMany(
        Permission, skip_reverse=True
    )


class User(ormar.Model):
    class Meta:
        database = database
        metadata = metadata
        tablename = "users"
        # constraints = [ormar.UniqueColumns("username", "email")]

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=50, unique=True)
    hashed_password: str = ormar.String(max_length=255, unique=True)
    email: typing.Optional[pydantic.EmailStr] = ormar.String(
        default=None, max_length=255, nullable=True, unique=True
    )
    first_name: typing.Optional[str] = ormar.String(
        default=None, max_length=255, nullable=True
    )
    last_name: typing.Optional[str] = ormar.String(
        default=None, max_length=255, nullable=True
    )
    midl_name: typing.Optional[str] = ormar.String(
        default=None, max_length=255, nullable=True
    )
    is_superuser: bool = ormar.Boolean(default=False)
    is_staff: bool = ormar.Boolean(default=False)
    is_active: bool = ormar.Boolean(default=False)
    joined_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    last_login_date: typing.Optional[datetime.datetime] = ormar.DateTime(
        default=None, nullable=True
    )
    comment: typing.Optional[typing.Text] = ormar.Text(default=None, nullable=True)
    groups: typing.Optional[typing.List[Group]] = ormar.ManyToMany(
        Group, skip_reverse=True
    )
