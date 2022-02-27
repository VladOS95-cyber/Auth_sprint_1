from http import HTTPStatus
from flask import jsonify
import uuid

import pytest

from auth.models import Role

from ..testdata.roles import role_by_id_expected, roles_list


@pytest.fixture
def create_role(session):

    roles_to_delete = []

    def _create_role(roles_list):
        session.bulk_save_objects(Role(**role_data) for role_data in roles_list)
        roles_to_delete.extend(role['id'] for role in roles_list)
        session.commit()

    yield _create_role

    session.query(Role).filter(Role.id.in_(roles_to_delete)).delete()
    session.commit()


def test_get_role_list(create_role, headers_with_admin_access, client, roles_list, session):
    create_role(roles_list)
    response = client.get(
        'api/v1/role',
        headers=headers_with_admin_access,
        )
    assert response.status_code == HTTPStatus.OK
    assert response.json.get('roles') == roles_list


def test_create_role(client, headers_with_admin_access, session):
    response = client.post(
        'api/v1/role',
        json={'code': 'test_role', 'description': 'for test'},
        headers=headers_with_admin_access
    )
    assert response.status_code == HTTPStatus.CREATED


def test_create_role_without_admin_permission(client, headers_with_user_access, session):
    response = client.post(
        'api/v1/role',
        json={'code': 'test_role', 'description': 'for test'},
        headers=headers_with_user_access)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_role_by_id(create_role, client, roles_list, headers_with_admin_access, role_by_id_expected, session):
    create_role(roles_list)
    response = client.get(
        'api/v1/role/a9c6e8da-f2bf-458a-978b-d2f50a031451',
        headers=headers_with_admin_access,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json.get('role') == role_by_id_expected


def test_get_non_existing_role_by_id(client, session):
    response = client.get('api/v1/role/444433332222')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_chage_role_details(create_role, client, roles_list, headers_with_admin_access, role_by_id_expected, session):
    create_role(roles_list)
    response = client.patch(
        'api/v1/role/a9c6e8da-f2bf-458a-978b-d2f50a031451',
        json={'code': 'admin', 'description': 'unlimited access to all actions'},
        headers=headers_with_admin_access,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json.get('role') == role_by_id_expected


def test_delete_role(create_role, client, roles_list, headers_with_admin_access, session):
    create_role(roles_list)
    response = client.delete(
        'api/v1/role/7cf56926-054c-4522-ac6f-d9f5d0e9d18e',
        headers=headers_with_admin_access
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_role_without_admin_permissions(create_role, client, roles_list, headers_with_user_access, session):
    create_role(roles_list)
    response = client.delete(
        'api/v1/role/7cf56926-054c-4522-ac6f-d9f5d0e9d18e',
        headers=headers_with_user_access
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_assign_roles(create_role, client, roles_list, login_user, session):
    create_role(roles_list)
    user, tokens = login_user('user1', '234')
    role_ids = [uuid.UUID(key['id']) for key in roles_list]
    access_token = tokens['access_token']
    response = client.post(
        'api/v1/assign-roles',
        json={
            'user_id': user.id,
            'role_ids': role_ids
        },
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == HTTPStatus.CREATED


def test_assign_roles_without_admin_permissions(create_role, client, roles_list, login_user, session):
    create_role(roles_list)
    user, tokens = login_user('user1', '234', is_superuser=False)
    role_ids = [uuid.UUID(key['id']) for key in roles_list]
    access_token = tokens['access_token']
    response = client.post(
        'api/v1/assign-roles',
        json={
            'user_id': user.id,
            'role_ids': role_ids
        },
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_check_permissions(client, headers_with_admin_access, session):
    response = client.post(
        'api/v1/check-permissions',
        json={
            "user_id": "8f4233c3-6284-41bd-af5a-737c6a3dc38d",
            "role_ids": [
                "73fdfb99-9465-4736-8661-af9f05d7991e",
                "d4cb21a9-77e4-42df-b79e-4fb25e4ea046"]
        },
        headers=headers_with_admin_access)
    assert response.status_code == HTTPStatus.OK
    assert response.json.get('has_permissions') is True


def test_check_permissions_without_admin_permission(client, headers_with_user_access, session):
    response = client.post(
        'api/v1/check-permissions',
        json={
            "user_id": "8f4233c3-6284-41bd-af5a-737c6a3dc38d",
            "role_ids": [
                "73fdfb99-9465-4736-8661-af9f05d7991e",
                "d4cb21a9-77e4-42df-b79e-4fb25e4ea046"]
        },
        headers=headers_with_user_access)
    assert response.status_code == HTTPStatus.FORBIDDEN
