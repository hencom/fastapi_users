from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import schemas
from services import audit_crud
from models import db

audit_router = APIRouter(
    prefix="/ehouse/api/auth/audit",
    tags=["Audit"],
)


@audit_router.get("/{table_name}")
def get_audit(
    table_name: str,
    limit: int = 100,
    skip: int = 0,
    db: Session = Depends(db.get_db),
):
    return audit_crud.get_audit_table(
        table_name=table_name, db=db, limit=limit, skip=skip
    )
