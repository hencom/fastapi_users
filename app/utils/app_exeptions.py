from typing import Any
from fastapi import HTTPException, status


def exception_not_found(detail: str = "Not Found"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def exception_duplicate(detail: str = "Already exist"):
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def exception_not_acceptable(detail: dict):
    return HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def exception_integrity_error(detail: Any):
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def exception_unauthorized(detail: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def exception_inactive_user(detail: str = "inactive user"):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


# def exception_inactive_user(detail: str = "inactive user"):
#     return HTTPException(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         detail=detail,
#         headers={"WWW-Authenticate": "Bearer"},
#     )


def exception_forbidden(detail: str = "FORBIDDEN"):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def exception_validate_jwt(
    detail: str = "Could not validate credentials",
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_426_UPGRADE_REQUIRED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def exception_password_not_match(
    detail: str = "password does not match the template",
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
