from dataclasses import dataclass

import pytest
from flask.testing import FlaskClient
from sqlalchemy import select
from sqlalchemy.engine import Connection

from web_app_models import User


def test_register_returns_details_with_auth_token(
    client: FlaskClient, connection: Connection
) -> None:
    response = client.post(
        "/register",
        json={
            "email": "test+register@safecorners.io",
            "password": "password",
        },
    )

    assert response.status_code == 200
    user = connection.execute(
        select(User).where(User.email == "test+register@safecorners.io")
    ).first()
    assert user is not None


@dataclass
class RegisteredUser:
    email: str
    password: str


@pytest.fixture()
def registered_user(client: FlaskClient) -> RegisteredUser:
    client.post(
        "/register",
        json={"email": "test+login@safecorners.io", "password": "password"},
    )
    if client.cookie_jar:
        client.cookie_jar.clear()
    return RegisteredUser(
        email="test+login@safecorners.io",
        password="password",
    )


def test_login(client: FlaskClient, registered_user: RegisteredUser) -> None:
    response = client.post(
        "/login?include_auth_token",
        json={"email": registered_user.email, "password": registered_user.password},
    )

    assert response.status_code == 200

    assert isinstance(
        response.json["response"]["user"].pop("authentication_token"), str
    )
