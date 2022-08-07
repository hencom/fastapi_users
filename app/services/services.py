from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import asyncpg

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme_refresh = OAuth2PasswordBearer(tokenUrl="refresh")

from models import user_models
from schemas import users as users_schemas

from . import njwt

# from . import schemas
from . import security


# async def get_user(username: str) -> models.User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Not Found",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     user = await models.User.objects.get_or_none(username=username)
#     if not user:
#         raise credentials_exception
#     return user


# async def create_user(user: users_schemas.UserCreate) -> models.User:
#     hashed_password = security.get_password_hash(user.password)
#     print(hashed_password)
#     try:
#         return await models.User.objects.create(
#             username=user.username, hashed_password=hashed_password
#         )
#     except asyncpg.exceptions.UniqueViolationError as ex:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail=ex.as_dict(),
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# def authenticate_user(username: str, password: str):
#     user = get_user(username)
#     if not user:
#         return False
#     if not security.verify_password(password, user.hashed_password):
#         return False
#     return user


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     payload = await njwt.get_data_from_token(token=token)
#     print(payload)
#     username: str = payload.get("user_id")
#     if username is None:
#         raise credentials_exception
#     token_data = schemas.TokenData(username=username)

#     user = get_user(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def refresh_token(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     payload = await njwt.get_data_from_token(token=token)
#     print(payload)
#     username: str = payload.get("user_id")
#     if username is None:
#         raise credentials_exception
#     token_data = schemas.TokenData(username=username)

#     user = get_user(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(
#     current_user: schemas.User = Depends(get_current_user),
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
