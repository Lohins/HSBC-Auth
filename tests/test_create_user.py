from http import HTTPStatus
from passlib.hash import sha256_crypt
from tests.utils import create_test_user, TEST_USER_NAME, TEST_PASSWORD
from auth.models.user import User
from auth.models.utils import DataStorage


def test_create_user(client):
    create_test_user(client, name=TEST_USER_NAME, password=TEST_PASSWORD)

def test_create_duplicated_user(client):
    create_test_user(client, name=TEST_USER_NAME, password=TEST_PASSWORD)

    # try to create an user that existed.
    json = {
        "user_name": TEST_USER_NAME,
        "password": TEST_PASSWORD
    }
    res = client.post(
        '/auth/user',
        json=json
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'User does exist!'

    

def test_password_stored_in_encrypted_way(client):
    create_test_user(client, name=TEST_USER_NAME, password=TEST_PASSWORD)

    user = DataStorage.users_table[0]

    assert sha256_crypt.verify(TEST_PASSWORD, user.password_hash)
