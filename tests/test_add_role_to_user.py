from http import HTTPStatus
from tests.utils import create_test_role, create_test_user, TEST_ROLE_NAME, TEST_USER_NAME

def test_add_role_to_an_non_existed_user(client):
    role = create_test_role(client)
    # no user created.

    res = client.post(
        '/auth/user/role',
        json={
            'user_name': TEST_USER_NAME,
            'role_name': role.name
        }
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'User does not exist!'

def test_add_an_non_existed_role_to_user(client):
    user = create_test_user(client)
    # no role created.

    res = client.post(
        '/auth/user/role',
        json={
            'user_name': user.name,
            'role_name': TEST_ROLE_NAME
        }
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Role does not exist!'


def test_add_role_to_user(client):
    role = create_test_role(client)
    user = create_test_user(client)

    # add role to the user
    res = client.post(
        '/auth/user/role',
        json={
            'user_name': user.name,
            'role_name': role.name
        }
    )

    assert res.status_code == HTTPStatus.OK
    assert res.get_data(as_text=True) == 'Done'

    # add role to the user again, and nothing should happen
    res = client.post(
        '/auth/user/role',
        json={
            'user_name': user.name,
            'role_name': role.name
        }
    )

    assert res.status_code == HTTPStatus.OK
    assert res.get_data(as_text=True) == 'Done'




