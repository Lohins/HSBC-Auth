from http import HTTPStatus
from tests.utils import create_test_user, TEST_USER_NAME, TEST_PASSWORD


def test_delete_an_existing_user(client):
    create_test_user(client, name=TEST_USER_NAME, password=TEST_PASSWORD)

    res = client.delete(
        '/auth/user',
        json={
            "user_name": TEST_USER_NAME
        }
    )

    assert res.status_code == HTTPStatus.NO_CONTENT


def test_delete_an_non_existed_user(client):
    res = client.delete(
        '/auth/user',
        json={
            "user_name": TEST_USER_NAME
        }
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'User does not exist!'
