import pytest


@pytest.fixture
def roles_list():
    return [
        {
            "id": "a9c6e8da-f2bf-458a-978b-d2f50a031451",
            "code": "admin",
            "description": "unlimited access to all actions",
        },
        {
            "id": "7cf56926-054c-4522-ac6f-d9f5d0e9d18e",
            "code": "subscriber",
            "description": "account without paying for registered users",
        },
        {
            "id": "7166fd5f-a4e4-45f0-952c-78d0297c7b03",
            "code": "member",
            "description": "account with payment options",
        },
    ]


@pytest.fixture
def role_by_id_expected():
    return {
        "id": "a9c6e8da-f2bf-458a-978b-d2f50a031451",
        "code": "admin",
        "description": "unlimited access to all actions"
    }


@pytest.fixture
def assigned_roles_to_user():
    return {
        "user_roles": [
            {
                "id": "4a73b964-af72-4801-aed9-113783561540",
                "user_id": "7cd483e9-5888-40fd-813a-a382154bcfd2",
                "role_id": "a9c6e8da-f2bf-458a-978b-d2f50a031451"
            },
            {
                "id": "4a73b964-af72-4801-aed9-113783561540",
                "user_id": "7cd483e9-5888-40fd-813a-a382154bcfd2",
                "role_id": "a9c6e8da-f2bf-458a-978b-d2f50a031451"
            }
        ]
    }
