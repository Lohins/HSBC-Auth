import pytest
from app import create_app
from auth.models.user import User
from auth.models.role import Role
from auth.models.utils import DataStorage

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True
    })

    yield app

    # 清除数据
    DataStorage.users_table = []
    DataStorage.roles_table = []
    DataStorage.user_role_table = []
    DataStorage.user_token_table = []

@pytest.fixture()
def client(app):
    return app.test_client()