import pytest


@pytest.fixture
def permissions_list():
    return [
        "/login",
        "/logout",
        "/film",
        "/admin",
        "/users"
        "/roles"
    ]
