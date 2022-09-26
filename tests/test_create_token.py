from http import HTTPStatus
from freezegun import freeze_time
from datetime import datetime, timedelta
from tests.utils import create_test_user, TEST_USER_NAME, TEST_PASSWORD
from auth.models.user import User
from auth.models.utils import DataStorage
from auth.config import Config


FIXED_TIME = datetime(2022, 10, 1, 0, 0, 0)
EXPIRED_TIME = datetime(2022, 10, 1, Config.TOKEN_EXPIRY_IN_HOURS, 0, 1)

def test_create_token_for_non_existed_user(client):
    res = client.post(
        '/auth/token',
        json={
            "user_name": TEST_USER_NAME,
            "password": TEST_PASSWORD
        }
    )

    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.get_data(as_text=True) == 'The user name and password do not match.'


def test_create_token_with_incorrect_credentials(client):
    res = client.post(
        '/auth/token',
        json={
            "user_name": TEST_USER_NAME,
            "password": 'INCORRECT PASSWORD'
        }
    )

    assert res.status_code == HTTPStatus.UNAUTHORIZED
    assert res.get_data(as_text=True) == 'The user name and password do not match.'

def test_create_token(client):
    with freeze_time(FIXED_TIME):
        create_test_user(client)

        res = client.post(
            '/auth/token',
            json={
                "user_name": TEST_USER_NAME,
                "password": TEST_PASSWORD
            }
        )

        json = res.json
        actual_expired_at_timestamp = json['expired_at']
        expected_expired_at = datetime.now() + timedelta(hours=Config.TOKEN_EXPIRY_IN_HOURS)
        assert res.status_code == HTTPStatus.CREATED
        assert 'token' in json
        
        # confirm the expired date is correct in the response.
        assert expected_expired_at.timestamp() == actual_expired_at_timestamp

        # confirm the expired date is correct in the memory.
        token = DataStorage.user_token_table[0]
        assert token.is_expired() == False
        assert token.expired_at.timestamp() == actual_expired_at_timestamp

    
    # time-travel to the future after 2 hours, the token should be expired.
    with freeze_time(EXPIRED_TIME):
        assert datetime.now().timestamp() > actual_expired_at_timestamp
        assert datetime.now().timestamp() > token.expired_at.timestamp()
        assert token.is_expired() == True
