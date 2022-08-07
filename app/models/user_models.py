import datetime
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Table,
    DateTime,
    event,
    JSON,
)
from sqlalchemy.orm import relationship, backref

from schemas import schemas
from .db import Base, SessionLocal


permissions_groups = Table(
    "permissions_groups",
    Base.metadata,
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

users_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)


class AssociationPermissionsGroups(Base):
    __tablename__ = "association_permissions_groups"

    permission_id = Column(ForeignKey("permissions.id"), primary_key=True)
    group_id = Column(ForeignKey("groups.id"), primary_key=True)


class AssociationUsersGroups(Base):
    __tablename__ = "association_users_groups"

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    group_id = Column(ForeignKey("groups.id"), primary_key=True)


class RefreshTokenBlackList(Base):
    __tablename__ = "refresh_token_black_list"

    id = Column(Integer, primary_key=True, index=True)
    refresh_token = Column(String, unique=True, index=True)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    comment = Column(Text, default=None, nullable=True)

    def __repr__(self) -> str:
        return f"<Permission {self.name}>"


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    comment = Column(Text, default=None, nullable=True)
    permissions = relationship(
        "Permission",
        secondary="association_permissions_groups",
        backref=backref(
            "groups",
            lazy="subquery",
        ),
    )
    users = relationship(
        "User",
        secondary="association_users_groups",
        backref=backref("groups", lazy="subquery"),
    )

    def __repr__(self) -> str:
        return f"<Group {self.name}>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_root = Column(Boolean, default=True)
    first_name = Column(String, default=None, nullable=True)
    last_name = Column(String, default=None, nullable=True)

    joined_date = Column(DateTime, default=datetime.datetime.now())
    last_login_date = Column(DateTime, default=None, nullable=True)

    comment = Column(Text, default=None, nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    @property
    def permissions(self):
        result = set()
        for group in self.groups:
            result = result.union(group.permissions)
        return list(result)

    def has_permission(self, pemission_name: str) -> bool:
        for p in self.permissions:
            if p.name == pemission_name:
                return True
        return False


class AuditTable(Base):
    __tablename__ = "audit"

    id = Column(Integer, primary_key=True, index=True)
    history_type = Column(String)
    table_name = Column(String)
    history_date = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, index=True)
    data = Column(JSON)


# @event.listens_for(Permission, "after_update", propagate=True)
# def my_listener_function(mapper, conection, model):
#     print("=======after_update Permission========", mapper, conection, model)
#     # print(model.name, model.comment)
#     # print(type(model.groups), dir(model.groups), model.groups.all())


# @event.listens_for(Permission, "after_delete", propagate=True)
# def my_listener_function(mapper, conection, model):
#     print("=======after_delete Permission========", mapper, conection, model)
#     # print(model.name, model.comment)
#     # print(type(model.groups), dir(model.groups), model.groups.all())


# @event.listens_for(AssociationPermissionsGroups, "after_insert", propagate=True)
# def permissions_groups_event(mapper, conection, model):
#     print(
#         "======= after_insert AssociationPermissionsGroups ========",
#         mapper,
#         conection,
#         model,
#     )


# @event.listens_for(User, "after_insert", propagate=True)
# def users_event(mapper, conection, model):
#     print(
#         "======= after_insert User ========",
#         mapper,
#         conection,
#         model,
#     )
#     # print(model.name, model.comment)
#     # print(type(model.groups), dir(model.groups), model.groups.all())


# @event.listens_for(Group.permissions, "append", propagate=True)
# def receive_set(target, value, initiator):
#     print(target, value, "=========Group.permissions append=========")


# @event.listens_for(Group.permissions, "remove", propagate=True)
# def receive_set(target, value, initiator):
#     print(target, value, "=========Group.permissions deleted=========")
