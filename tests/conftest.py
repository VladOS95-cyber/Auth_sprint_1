import json
from http import HTTPStatus

import pytest

from auth.app import create_app, db
from auth.models import User

from . import config


@pytest.fixture
def app():
    return create_app(config=config)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session():
    yield db.session
    db.session.remove()
    db.drop_all()


@pytest.fixture
def create_user(session):

    created_records = []

    def _create_user(username, password, is_superuser=True, **kwargs):
        user = User(username=username, password=password, is_superuser=is_superuser)
        for key, value in kwargs.items():
            setattr(user, key, value)
        created_records.append(username)
        session.add(user)
        session.commit()
        return user

    yield _create_user

    for username in created_records:
        User.query.filter_by(username=username).delete()
    session.commit()


@pytest.fixture
def login_user(client, create_user):
    # create user
    # login
    # return tokens

    def _login_user(username, password, **kwargs):
        user = create_user(username, password, **kwargs)
        body = json.dumps({'username': username, 'password': password})
        response = client.post(
            '/api/v1/auth/login',
            data=body,
            content_type='application/json',
        )

        if response.status_code == HTTPStatus.OK:
            return user, response.json['tokens']
        else:
            raise Exception('Bad login request')

    return _login_user


@pytest.fixture
def headers_with_admin_access(client, login_user):
    _, tokens = login_user(username='test_admin', password='admin')
    access_token = tokens['access_token']
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def headers_with_user_access(client, login_user):
    _, tokens = login_user(username='test_user', password='user', is_superuser=False)
    access_token = tokens['access_token']
    return {'Authorization': f'Bearer {access_token}'}
