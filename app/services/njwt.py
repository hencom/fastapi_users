from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status

from settings import security_settings
from utils import app_exeptions


# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_JWT_SUBJECT = "access"
# REFRESH_TOKEN_JWT_SUBJECT = "refresh"


def create_jwt_token(data: dict, token_type: str, expires_delta: int | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": data.get("sub"), "type": token_type})
    encoded_jwt = jwt.encode(
        to_encode, security_settings.SECRET_KEY, algorithm=security_settings.ALGORITHM
    )
    return encoded_jwt


def get_data_from_token(token: str):
    try:
        return jwt.decode(
            token,
            security_settings.SECRET_KEY,
            algorithms=[security_settings.ALGORITHM],
        )
    except JWTError:
        raise app_exeptions.exception_validate_jwt()
