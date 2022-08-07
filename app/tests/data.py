class Permission(object):
    result = {}

    def set_permission_name(self, ermission_name: str) -> None:
        self.result["name"] = ermission_name

    def set_comment(self, comment: str) -> None:
        self.result["comment"] = comment

    def set_group_list(self, group_name_list: list) -> None:
        self.result["group_name_list"] = group_name_list

    def build(self) -> dict:
        return self.result


p1_data = {"name": "test_p1", "comment": "comment test_p1", "group_name_list": []}
p2_data = {"name": "test_p2", "comment": "comment test_p2", "group_name_list": []}
p3_data = {
    "name": "test_p3",
    "comment": "comment test_p3",
    "group_name_list": ["test_g2", "test_g1"],
}

p4_data = {
    "name": "test_p4",
    "comment": "comment test_p4",
    "group_name_list": ["test_g1"],
}

g1_data = {
    "name": "test_g1",
    "comment": "comment test_g1",
    "permission_name_list": ["test_p1", "test_p2"],
}
g2_data = {
    "name": "test_g2",
    "comment": "comment test_g2",
    "permission_name_list": [
        "test_p2",
    ],
}
g3_data = {
    "name": "test_g3",
    "comment": "comment test_g2",
    "permission_name_list": [
        "test_p1",
    ],
}


user1_data = {
    "email": "test1_user@example.com",
    "username": "test_user1",
    "is_active": True,
    "is_root": True,
    "first_name": "first_name1",
    "last_name": "last_name1",
    "comment": "comment1",
    "password": "123password",
    "group_name_list": ["test_g1", "test_g2"],
}

user2_data = {
    "email": "test2_user@example.com",
    "username": "test_user2",
    "is_active": True,
    "is_root": True,
    "first_name": "first_name2",
    "last_name": "last_name2",
    "comment": "comment2",
    "password": "123password",
    "group_name_list": [
        "test_g1",
    ],
}

user3_data = {
    "email": "test3_user@example.com",
    "username": "test_user3",
    "is_active": True,
    "is_root": False,
    "first_name": "first_name3",
    "last_name": "last_name3",
    "comment": "comment3",
    "password": "123password",
    "group_name_list": [
        "test_g2",
    ],
}
