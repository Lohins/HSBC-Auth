from http import HTTPStatus
from tests.utils import create_test_role, TEST_ROLE_NAME

def test_create_role(client):
    create_test_role(client, TEST_ROLE_NAME)

def test_create_duplicated_role(client):
    create_test_role(client, TEST_ROLE_NAME)

    # duplicated role.
    res = client.post(
        '/auth/role',
        json={
            "role_name": TEST_ROLE_NAME
        }
    )
    
    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.get_data(as_text=True) == 'Role does exist!'



