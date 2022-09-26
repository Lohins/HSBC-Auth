import json
from flask import Blueprint, request
from http import HTTPStatus
from auth.models.token import Token, TokenExipredError, TokenNotFoundError
from auth.models.user import User, UserDuplicatedError, UserNotFoundError, AuthenticateFailError
from auth.models.role import Role, RoleDuplicatedError, RoleNotFoundError


auth_blueprint = Blueprint('Auth API', __name__, url_prefix='/auth')

@auth_blueprint.route('/user', methods=['POST'])
def create_user():
    data = request.json
    try:
        User.create_user(data['user_name'], data['password'])
    except UserDuplicatedError as e:
        return 'User does exist!', HTTPStatus.BAD_REQUEST

    return 'Created', HTTPStatus.CREATED

@auth_blueprint.route('/user', methods=['DELETE'])
def delete_user():
    data = request.json

    try:
        User.delete_user(data['user_name'])
    except UserNotFoundError as e:
        return 'User does not exist!', HTTPStatus.BAD_REQUEST

    return 'Deleted', HTTPStatus.NO_CONTENT


@auth_blueprint.route('/role', methods=['POST'])
def create_role():
    data = request.json

    try:
        Role.create_role(data['role_name'])
    except RoleDuplicatedError as e:
        return 'Role does exist!', HTTPStatus.BAD_REQUEST

    return 'Created', HTTPStatus.CREATED


@auth_blueprint.route('/role', methods=['DELETE'])
def delete_role():
    data = request.json

    try:
        Role.delete_role(data['role_name'])
    except RoleNotFoundError as e:
        return 'Role does not exist!', HTTPStatus.BAD_REQUEST

    return 'Deleted', HTTPStatus.NO_CONTENT


@auth_blueprint.route('/user/role', methods=['POST'])
def add_role_to_user():
    data = request.json
    user_name = data['user_name']
    role_name = data['role_name']

    user = User.get_user(user_name)

    if not user:
        return 'User does not exist!', HTTPStatus.BAD_REQUEST

    role = Role.get_role(role_name)
    if not role:
        return 'Role does not exist!', HTTPStatus.BAD_REQUEST

    user.add_role(role)

    return 'Done', HTTPStatus.OK


@auth_blueprint.route('/token', methods=['POST'])
def create_token():
    data = request.json
    user_name = data['user_name']
    password = data['password']

    try:
        token = User.authenticate(user_name, password)

        return {
            'token': token.token,
            'expired_at': token.expired_at.timestamp()
        }, HTTPStatus.CREATED
    except (AuthenticateFailError, UserNotFoundError) as e:
        return 'The user name and password do not match.', HTTPStatus.UNAUTHORIZED


@auth_blueprint.route('/token', methods=['DELETE'])
def invalidate_token():
    data = request.json

    try:
        Token.invalidate_token(data['token'])
    except TokenNotFoundError as e:
        return 'Token does not exist.', HTTPStatus.BAD_REQUEST
    except TokenExipredError as e:
        return 'Token has been expired.', HTTPStatus.BAD_REQUEST

    return 'Done', HTTPStatus.OK


@auth_blueprint.route('/role_check', methods=['GET'])
def check_role():
    data = request.json

    token = data['token']
    role_name = data['role']

    try:
        result = User.check_role(token, role_name)
    except TokenNotFoundError as e:
        return 'Token does not exist.', HTTPStatus.BAD_REQUEST
    except TokenExipredError as e:
        return 'Token has been expired.', HTTPStatus.BAD_REQUEST


    return { 'result': result }, HTTPStatus.OK


@auth_blueprint.route('/roles', methods=['GET'])
def get_all_roles():
    data = request.json

    token = data['token']

    try:
        all_roles = User.get_all_roles(token)
    except TokenNotFoundError as e:
        return 'Token does not exist.', HTTPStatus.BAD_REQUEST
    except TokenExipredError as e:
        return 'Token has been expired.', HTTPStatus.BAD_REQUEST

    return { 'roles': all_roles }, HTTPStatus.OK
