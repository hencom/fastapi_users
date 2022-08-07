import json
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from schemas import schemas
from services import users_crud


def access_token(client: TestClient, username: str, password: str) -> json:
    response = client.post(
        "/ehouse/api/auth/users/token",
        data={"username": username, "password": password},
    )
    return response.json()


def ctreate_user(
    new_user: schemas.UserCteate,
    db: Session,
):
    db_user = users_crud.create_user(user=new_user, db=db)
    return schemas.UserDetail(
        username=db_user.username,
        id=db_user.id,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        is_active=db_user.is_active,
        is_root=db_user.is_root,
        last_login_date=db_user.last_login_date,
        joined_date=db_user.joined_date,
        comment=db_user.comment,
        groups=db_user.groups,
    )


def delete_user_db(
    username: str,
    db: Session,
) -> None:
    users_crud.delete_user(username=username, db=db)


def delete_user(client: TestClient, token: str, user_name: str):
    response = client.delete(
        f"/ehouse/api/auth/users/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def create_permission(client: TestClient, token: str, data: json):
    response = client.post(
        "/ehouse/api/auth/permissions/",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    return response


def update_permission(client: TestClient, token: str, data: json, permission_name: str):
    response = client.put(
        f"/ehouse/api/auth/permissions/{permission_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    return response


def create_group(client: TestClient, token: str, data: json):
    response = client.post(
        "/ehouse/api/auth/groups/",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    return response


def update_group(client: TestClient, token: str, data: json, group_name: str):
    response = client.put(
        f"/ehouse/api/auth/groups/{group_name}",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    return response


def create_user(client: TestClient, token: str, data: json):
    response = client.post(
        "/ehouse/api/auth/users/",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    return response


def update_user(client: TestClient, token: str, data: json, username: str):
    response = client.put(
        f"/ehouse/api/auth/users/{username}",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    return response


def delete_permission(client: TestClient, token: str, permission_name: str):
    response = client.delete(
        f"/ehouse/api/auth/permissions/{permission_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def get_permission(client: TestClient, token: str, permission_name: str):
    response = client.get(
        f"/ehouse/api/auth/permissions/{permission_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def delete_group(client: TestClient, token: str, group_name: str):
    response = client.delete(
        f"/ehouse/api/auth/groups/{group_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def delete_user(client: TestClient, token: str, user_name: str):
    response = client.delete(
        f"/ehouse/api/auth/users/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def change_password_for_current_user(
    client: TestClient, token: str, old_password: str, new_password: str
):
    response = client.post(
        f"/ehouse/api/auth/users/me/change-password?old_password={old_password}&new_password={new_password}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def reset_password(client: TestClient, token: str, new_password: str, username: str):
    response = client.post(
        f"http://127.0.0.1:8080/ehouse/api/auth/users/{username}/reset-password?new_password={new_password}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def get_group(client: TestClient, token: str, group_name: str):
    response = client.get(
        f"/ehouse/api/auth/groups/{group_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def get_permission(client: TestClient, token: str, permission_name: str):
    response = client.get(
        f"/ehouse/api/auth/permissions/{permission_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def get_user(client: TestClient, token: str, user_name: str):
    response = client.get(
        f"/ehouse/api/auth/users/{user_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response


def get_audit(client: TestClient, token: str, table_name: str):
    response = client.get(
        f"/ehouse/api/auth/audit/{table_name}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response
