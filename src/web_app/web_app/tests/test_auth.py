from dataclasses import dataclass

import pytest
from flask import testing


def test_register_returns_details_with_auth_token(client: testing.FlaskClient) -> None:
    response = client.post(
        "/register",
        json={"email": "test+register@safecorners.io", "password": "password"},
    )

    assert response.status_code == 200
    json_response_body = response.json.copy()
    assert isinstance(
        json_response_body["response"]["user"].pop("authentication_token"), str
    )
    assert isinstance(json_response_body["response"]["user"].pop("id"), str)
    assert json_response_body == {"meta": {"code": 200}, "response": {"user": {}}}


@dataclass
class RegisteredUser:
    email: str
    password: str
    id: str


@pytest.fixture()
def registered_user(client: testing.FlaskClient) -> RegisteredUser:
    response = client.post(
        "/register",
        json={"email": "test+login@safecorners.io", "password": "password"},
    )
    client.cookie_jar.clear()
    return RegisteredUser(
        email="test+login@safecorners.io",
        password="password",
        id=response.json["response"]["user"]["id"],
    )


def test_login(client: testing.FlaskClient, registered_user: RegisteredUser) -> None:
    response = client.post(
        "/login",
        json={"email": registered_user.email, "password": registered_user.password},
    )

    assert response.status_code == 200
    json_response_body = response.json.copy()
    json_response_body["response"]["user"].pop("authentication_token")
    assert json_response_body == {
        "meta": {"code": 200},
        "response": {"user": {"id": registered_user.id}},
    }
