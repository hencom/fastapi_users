import json
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session, dynamic
from sqlalchemy import event
from . import db_services, group_crud, users_crud

from models import user_models
from schemas import schemas

from utils import app_exeptions

from models import db


def create_audit(
    table_name: str,
    data_json: json,
    history_type: str,
    db: Session,
    user: schemas.User,
) -> None:
    db_audit = user_models.AuditTable(
        history_type=history_type,
        user_id=user.id,
        data=data_json,
        table_name=table_name,
    )
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)


def get_audit_table(table_name: str, db: Session, skip: int = 0, limit: int = 100):
    db_audit = (
        db.query(user_models.AuditTable)
        .filter(user_models.AuditTable.table_name == table_name)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return db_audit


def get_audit_list(db: Session, skip: int = 0, limit: int = 100):
    db_audit = db.query(user_models.AuditTable).offset(skip).limit(limit).all()
    return db_audit
