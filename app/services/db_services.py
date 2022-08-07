from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from utils import app_exeptions


def db_commit(db: Session):
    try:
        db.commit()
    except IntegrityError as ex:
        raise app_exeptions.exception_integrity_error(detail=ex.args)
