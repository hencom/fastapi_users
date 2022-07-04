from fastapi import HTTPException, status


def exception_not_found(detail: str = "Not Found"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def exception_not_acceptable(detail: dict):
    return HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
