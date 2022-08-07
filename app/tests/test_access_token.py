from fastapi import status
from services import njwt


def test_login_for_access_token(client, access_token, username, password):
    response = client.post(
        "/ehouse/api/auth/users/token",
        data={"username": username, "password": password},
    )
    resp_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert resp_json.get("token_type") == "bearer"
    access_token_data = njwt.get_data_from_token(token=resp_json.get("access_token"))
    assert access_token_data.get("sub") == username
    assert access_token_data.get("type") == "access"

    refresh_token_data = njwt.get_data_from_token(token=resp_json.get("refresh_token"))
    assert refresh_token_data.get("sub") == username
    assert refresh_token_data.get("type") == "refresh"


def test_login_wrong_password(client, username):
    response = client.post(
        "/ehouse/api/auth/users/token",
        data={"username": username, "password": "111"},
    )
    resp_json = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp_json == {"detail": "Password is not correct"}


def test_login_wrong_username(client, password):
    response = client.post(
        "/ehouse/api/auth/users/token",
        data={"username": "qqq", "password": password},
    )
    resp_json = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert resp_json == {"detail": "User with username qqq not found"}


# def test_delete_user(client, username):
#     _db = next(client.app.dependency_overrides.get(db.get_db)())
#     utils.delete_user_db(db=_db, username=USERNAME)
