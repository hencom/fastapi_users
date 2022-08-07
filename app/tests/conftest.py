import os
import pytest
from fastapi.testclient import TestClient
from fastapi import status, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models.user_models import Base
from models import db
from schemas import schemas

from . import utils

USERNAME = "test_username"
PASSWORD = "password123"


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_client = TestClient(app)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def username():
    return USERNAME


@pytest.fixture(scope="session")
def password():
    return PASSWORD


@pytest.fixture(scope="session")
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[db.get_db] = override_get_db
    yield _client
    os.remove("./test.db")


@pytest.fixture(scope="session")
def access_token():
    new_user = schemas.UserCteate(
        email=None,
        username=USERNAME,
        is_active=True,
        is_root=True,
        first_name=None,
        last_name=None,
        comment=None,
        password=PASSWORD,
        group_name_list=None,
    )
    _db = next(override_get_db())
    utils.ctreate_user(new_user=new_user, db=_db)
    print("superuser successfully created")
    response = _client.post(
        "/ehouse/api/auth/users/token",
        data={"username": USERNAME, "password": PASSWORD},
    )
    return response.json().get("access_token")
