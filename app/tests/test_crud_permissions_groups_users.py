import json
from fastapi import status

import requests

from schemas import schemas

from . import utils
from . import data


def validate_permission(
    client, access_token, response: requests.models.Response, data: json
):
    groups = response.json().get("groups")
    assert response.json().get("name") == data.get("name")
    assert response.json().get("comment") == data.get("comment")
    assert isinstance(groups, list)
    assert len(groups) == len(data.get("group_name_list"))
    for g in data.get("group_name_list"):
        g_response = utils.get_group(client=client, token=access_token, group_name=g)
        assert schemas.BaseGroup(**g_response.json()).dict() in groups


def validate_group(
    client, access_token, response: requests.models.Response, data: json
):
    permissions = response.json().get("permissions")
    assert response.json().get("name") == data.get("name")
    assert response.json().get("comment") == data.get("comment")
    assert isinstance(permissions, list)
    assert len(permissions) == len(data.get("permission_name_list"))

    for p in data.get("permission_name_list"):
        p_response = utils.get_permission(
            client=client, token=access_token, permission_name=p
        )
        assert schemas.BasePermission(**p_response.json()).dict() in permissions


def validate_user(client, access_token, response: requests.models.Response, data: json):

    groups = response.json().get("groups")
    assert response.json().get("email") == data.get("email")
    assert response.json().get("username") == data.get("username")
    assert response.json().get("is_active") == data.get("is_active")
    assert response.json().get("is_root") == data.get("is_root")
    assert response.json().get("first_name") == data.get("first_name")
    assert response.json().get("last_name") == data.get("last_name")
    assert response.json().get("comment") == data.get("comment")
    for g in data.get("group_name_list"):
        g_response = utils.get_group(client=client, token=access_token, group_name=g)
        assert schemas.BaseGroup(**g_response.json()).dict() in groups


def test_create_permission_1(client, access_token):
    response = utils.create_permission(
        client=client,
        token=access_token,
        data=data.p1_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    validate_permission(client, access_token, response, data.p1_data)


def test_create_permission_1_duplicate(client, access_token):
    response = utils.create_permission(
        client=client,
        token=access_token,
        data=data.p1_data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_permission_2(client, access_token):
    response = utils.create_permission(
        client=client,
        token=access_token,
        data=data.p2_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    validate_permission(client, access_token, response, data.p2_data)


def test_create_group_1(client, access_token):
    response = utils.create_group(client=client, token=access_token, data=data.g1_data)
    assert response.status_code == status.HTTP_201_CREATED
    validate_group(client, access_token, response=response, data=data.g1_data)


def test_create_group_1_duplicate(client, access_token):
    response = utils.create_group(client=client, token=access_token, data=data.g1_data)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_group_2(client, access_token):
    response = utils.create_group(client=client, token=access_token, data=data.g2_data)
    assert response.status_code == status.HTTP_201_CREATED
    validate_group(client, access_token, response=response, data=data.g2_data)


def test_create_permission_3(client, access_token):
    response = utils.create_permission(
        client=client,
        token=access_token,
        data=data.p3_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    validate_permission(client, access_token, response, data.p3_data)


def test_create_user_1(client, access_token):
    user_resp = utils.create_user(
        client=client, token=access_token, data=data.user1_data
    )
    assert user_resp.status_code == status.HTTP_201_CREATED
    validate_user(
        client=client,
        access_token=access_token,
        response=user_resp,
        data=data.user1_data,
    )


def test_create_user_1_duplicate(client, access_token):
    user_resp = utils.create_user(
        client=client, token=access_token, data=data.user1_data
    )
    assert user_resp.status_code == status.HTTP_409_CONFLICT


def test_create_user_2(client, access_token):
    user_resp = utils.create_user(
        client=client, token=access_token, data=data.user2_data
    )
    assert user_resp.status_code == status.HTTP_201_CREATED
    validate_user(
        client=client,
        access_token=access_token,
        response=user_resp,
        data=data.user2_data,
    )


def test_update_user_1_exist(client, access_token):
    user_resp = utils.update_user(
        client=client,
        token=access_token,
        data=data.user2_data,
        username=data.user1_data.get("username"),
    )
    assert user_resp.status_code == status.HTTP_409_CONFLICT


def test_update_user_1(client, access_token):
    user_resp = utils.update_user(
        client=client,
        token=access_token,
        data=data.user3_data,
        username=data.user1_data.get("username"),
    )
    assert user_resp.status_code == status.HTTP_200_OK
    validate_user(
        client=client,
        access_token=access_token,
        response=user_resp,
        data=data.user3_data,
    )


def test_change_password_for_current_user(client, access_token):
    user_res = utils.change_password_for_current_user(
        client=client,
        token=access_token,
        old_password="password123",
        new_password="password456",
    )
    assert user_res.status_code == status.HTTP_202_ACCEPTED


def test_reset_password(client, access_token):
    user_res = utils.reset_password(
        client=client,
        token=access_token,
        username=data.user3_data.get('username'),
        new_password="password789",
    )
    assert user_res.status_code == status.HTTP_202_ACCEPTED


def test_get_permission(client, access_token):
    response = utils.get_permission(
        client=client, token=access_token, permission_name=data.p1_data.get("name")
    )
    assert response.status_code == status.HTTP_200_OK
    data.p1_data["group_name_list"] = [
        "test_g1",
    ]
    validate_permission(
        client=client, access_token=access_token, response=response, data=data.p1_data
    )


def test_update_permission_exist(client, access_token):
    response = utils.update_permission(
        client=client,
        token=access_token,
        data=data.p3_data,
        permission_name=data.p1_data.get("name"),
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_permission_1(client, access_token):
    response = utils.get_permission(
        client=client, token=access_token, permission_name=data.p1_data.get("name")
    )
    assert response.status_code == status.HTTP_200_OK
    validate_permission(
        client=client, access_token=access_token, response=response, data=data.p1_data
    )


def test_update_permission1(client, access_token):
    response = utils.update_permission(
        client=client,
        token=access_token,
        data=data.p4_data,
        permission_name=data.p1_data.get("name"),
    )
    assert response.status_code == status.HTTP_200_OK
    validate_permission(
        client=client, access_token=access_token, response=response, data=data.p4_data
    )


def test_update_permission2(client, access_token):
    response = utils.update_permission(
        client=client,
        token=access_token,
        data=data.p1_data,
        permission_name=data.p4_data.get("name"),
    )
    assert response.status_code == status.HTTP_200_OK
    validate_permission(
        client=client, access_token=access_token, response=response, data=data.p1_data
    )


def test_update_grop_exist(client, access_token):
    response = utils.update_group(
        client=client,
        token=access_token,
        data=data.g2_data,
        group_name=data.g1_data.get("name"),
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_grop_2(client, access_token):
    response = utils.update_group(
        client=client,
        token=access_token,
        data=data.g3_data,
        group_name=data.g2_data.get("name"),
    )
    assert response.status_code == status.HTTP_200_OK
    validate_group(
        client=client, access_token=access_token, response=response, data=data.g3_data
    )


def test_delete_groups(client, access_token):
    g1_response = utils.delete_group(
        client=client, token=access_token, group_name=data.g1_data.get("name")
    )
    g2_response = utils.delete_group(
        client=client, token=access_token, group_name=data.g3_data.get("name")
    )
    assert g2_response.status_code == status.HTTP_204_NO_CONTENT
    assert g1_response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_permissions(client, access_token):
    p1_response = utils.delete_permission(
        client=client, permission_name=data.p1_data.get("name"), token=access_token
    )
    p2_response = utils.delete_permission(
        client=client, permission_name=data.p2_data.get("name"), token=access_token
    )
    p3_response = utils.delete_permission(
        client=client, permission_name=data.p3_data.get("name"), token=access_token
    )
    assert p1_response.status_code == status.HTTP_204_NO_CONTENT
    assert p2_response.status_code == status.HTTP_204_NO_CONTENT
    assert p3_response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_users(client, access_token):
    user_resp = utils.delete_user(
        client=client, token=access_token, user_name=data.user3_data.get("username")
    )
    assert user_resp.status_code == status.HTTP_204_NO_CONTENT
    user_resp = utils.delete_user(
        client=client, token=access_token, user_name=data.user2_data.get("username")
    )
    assert user_resp.status_code == status.HTTP_204_NO_CONTENT
    # utils.delete_user_db(db=_db, username=USERNAME)


# def test_remove_test_db():
#     _db.close()
#     os.remove("./test.db")
