import http
from tests.utils import create_test_user, create_test_role, TEST_USER_NAME, TEST_PASSWORD, TEST_ROLE_NAME
from http import HTTPStatus
from freezegun import freeze_time
from datetime import datetime
from auth.config import Config


FIXED_TIME = datetime(2022, 10, 1, 0, 0, 0)
EXPIRED_TIME = datetime(2022, 10, 1, Config.TOKEN_EXPIRY_IN_HOURS, 0, 1)


def test_check_role_with_non_existed_token(client):
    # no token created.
    res = client.get(
        '/auth/role_check',
        json={
            "token": 'RANDOM',
            "role": TEST_ROLE_NAME
        }
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Token does not exist.'

def test_check_role_with_expired_token(client):
    with freeze_time(FIXED_TIME):
        # create use, role and token.
        user = create_test_user(client)
        role = create_test_role(client)

        res = client.post(
            '/auth/token',
            json={
                "user_name": TEST_USER_NAME,
                "password": TEST_PASSWORD
            }
        )

        token = res.json['token']  

        # add the role to user.
        client.post(
            '/auth/user/role',
            json={
                'user_name': user.name,
                'role_name': role.name
            }
        )      
    
    # check the role after 2 hours, the token should be expired.
    with freeze_time(EXPIRED_TIME):
        res = client.get(
            '/auth/role_check',
            json={
                "token": token,
                "role": TEST_ROLE_NAME
            }
        )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Token has been expired.'

def test_check_an_user_with_correct_role(client):
    # create use, role and token.
    user = create_test_user(client)
    role = create_test_role(client)

    res = client.post(
        '/auth/token',
        json={
            "user_name": TEST_USER_NAME,
            "password": TEST_PASSWORD
        }
    )
    token = res.json['token']

    # add the role to user.
    res = client.post(
        '/auth/user/role',
        json={
            'user_name': user.name,
            'role_name': role.name
        }
    )

    # check the role.
    res = client.get(
        '/auth/role_check',
        json={
            "token": token,
            "role": TEST_ROLE_NAME
        }
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json['result'] is True

def test_check_an_user_with_incorrect_role(client):
    # create use, role and token.
    user = create_test_user(client)
    role = create_test_role(client)

    res = client.post(
        '/auth/token',
        json={
            "user_name": TEST_USER_NAME,
            "password": TEST_PASSWORD
        }
    )
    token = res.json['token']

    # didn't add the role to user.

    # check the role.
    res = client.get(
        '/auth/role_check',
        json={
            "token": token,
            "role": TEST_ROLE_NAME
        }
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json['result'] is False