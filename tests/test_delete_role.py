from http import HTTPStatus
from tests.utils import create_test_role, TEST_ROLE_NAME


def test_delete_an_existing_role(client):
    create_test_role(client)

    res = client.delete(
        '/auth/role',
        json={
            "role_name": TEST_ROLE_NAME
        }
    )

    assert res.status_code == HTTPStatus.NO_CONTENT


def test_delete_an_non_existed_role(client):
    res = client.delete(
        '/auth/role',
        json={
            "role_name": TEST_ROLE_NAME
        }
    )

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Role does not exist!'
