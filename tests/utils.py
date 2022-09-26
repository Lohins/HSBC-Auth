from http import HTTPStatus
from auth.models.role import Role
from auth.models.user import User
from passlib.hash import sha256_crypt
from auth.models.utils import DataStorage


TEST_USER_NAME = 'Sitong'
TEST_PASSWORD = '123456'

TEST_ROLE_NAME = 'Admin'

def create_test_role(client, name=TEST_ROLE_NAME):
    res = client.post(
        '/auth/role',
        json={
            "role_name": name
        }
    )
    assert res.status_code == HTTPStatus.CREATED

    # confirm the data in memory is correct.
    role = list(filter(lambda r:r.name == name, DataStorage.roles_table))[0]
    assert role.name == name

    return role

def create_test_user(client, name=TEST_USER_NAME, password=TEST_PASSWORD):
    res = client.post(
        '/auth/user',
        json={
            "user_name": name,
            "password": password
        }
    )
    assert res.status_code == HTTPStatus.CREATED

    # confirm the data in memory is correct.
    user = list(filter(lambda u:u.name == name, DataStorage.users_table))[0]

    assert user.name == name
    assert sha256_crypt.verify(password, user.password_hash)

    return user
