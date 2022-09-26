from http import HTTPStatus
from freezegun import freeze_time
from datetime import datetime, timedelta
from tests.utils import create_test_user, TEST_USER_NAME, TEST_PASSWORD
from auth.config import Config
from auth.models.user import User
from auth.models.utils import DataStorage


FIXED_TIME = datetime(2022, 10, 1, 0, 0, 0)
EXPIRED_TIME = datetime(2022, 10, 1, Config.TOKEN_EXPIRY_IN_HOURS, 0, 1)

def test_invalidate_an_non_existed_token(client):
    res = client.delete(
        '/auth/token',
        json={
            "token": 'RANDOM'
        }
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Token does not exist.'

def test_invalidate_a_token(client):
    create_test_user(client)

    res = client.post(
        '/auth/token',
        json={
            "user_name": TEST_USER_NAME,
            "password": TEST_PASSWORD
        }
    )

    token = res.json['token']

    # invalidate the token.
    res = client.delete(
        '/auth/token',
        json={
            "token": token
        }
    )
    assert res.status_code == HTTPStatus.OK

    # try to invalidate this invalid token.
    res = client.delete(
        '/auth/token',
        json={
            "token": token
        }
    )
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Token has been expired.'
