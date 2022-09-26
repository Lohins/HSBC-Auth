import http
from tests.utils import create_test_user, create_test_role, TEST_USER_NAME, TEST_PASSWORD, TEST_ROLE_NAME
from http import HTTPStatus
from freezegun import freeze_time
from datetime import datetime
from auth.config import Config

FIXED_TIME = datetime(2022, 10, 1, 0, 0, 0)
EXPIRED_TIME = datetime(2022, 10, 1, Config.TOKEN_EXPIRY_IN_HOURS, 0, 1)

def test_all_roles_with_non_existed_token(client):
    # no token created.
    res = client.get(
        '/auth/roles',
        json={
            "token": 'RANDOM',
            "role": TEST_ROLE_NAME
        }
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Token does not exist.'

def test_all_roles_with_expired_token(client):
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
            '/auth/roles',
            json={
                "token": token,
                "role": TEST_ROLE_NAME
            }
        )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Token has been expired.'

def test_get_all_roles(client):
    # create use
    user = create_test_user(client)
    # create token.
    res = client.post(
        '/auth/token',
        json={
            "user_name": TEST_USER_NAME,
            "password": TEST_PASSWORD
        }
    )
    token = res.json['token']

    # create 3 roles: Admin, Member, Employer
    admin = create_test_role(client, name='Admin')
    member = create_test_role(client, name='Member')
    employer = create_test_role(client, name='Employer')
    # add roles (Admin & employer) to user.
    res = client.post(
        '/auth/user/role',
        json={
            'user_name': user.name,
            'role_name': admin.name
        }
    )
    res = client.post(
        '/auth/user/role',
        json={
            'user_name': user.name,
            'role_name': employer.name
        }
    )

    # check the role.
    res = client.get(
        '/auth/roles',
        json={
            "token": token,
        }
    )

    assert res.status_code == HTTPStatus.OK
    assert res.json['roles'] == ['Admin', 'Employer']

