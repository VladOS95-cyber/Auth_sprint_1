import uuid
from functools import wraps
from http import HTTPStatus

from flask import make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from extensions import db
from models import Permission, RolePermissions, UserRole, User


def get_user_id_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        raise ValueError('User not exists', username)

    return user.id


def get_user_permissions(user_id):
    permissions = db.session.query(
        Permission
    ).join(
        RolePermissions
    ).join(
        UserRole, UserRole.role_id == RolePermissions.role_id
    ).filter(
        UserRole.user_id == user_id
    ).all()

    return permissions


def get_tokens(user_id, token=None):

    if token is None:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError('User not exists', user_id)

        permissions = [permission.code for permission in get_user_permissions(user.id)]
        is_superuser = user.is_superuser
    else:
        permissions = token.get('permissions', [])
        is_superuser = token.get('is_superuser', False)

    additional_claims = {
        'permissions': permissions,
        'is_superuser': is_superuser,
    }

    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user_id, additional_claims=additional_claims)

    return access_token, refresh_token


def permission_required(permission):
    """
    Проверяем наличие у пользователя права на доступ к ресурсу. Это возможно в одном из случаев:
     - это суперпользователь
     - у пользователя есть необходимый permission
     - пользователь работает со своими данными

    :param permission:
    :return:
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            uri_user_id = kwargs.get('user_id')
            token_user_id = uuid.UUID(get_jwt_identity())
            permissions = claims.get('permissions', [])
            is_superuser = claims.get('is_superuser', False)
            is_owner = uri_user_id == token_user_id

            if is_superuser or is_owner or permission in permissions:
                return fn(*args, **kwargs)
            else:
                return make_response(
                    {
                        "message": "Permission denied",
                        "status": "error"
                    }, HTTPStatus.FORBIDDEN)

        return decorator

    return wrapper
