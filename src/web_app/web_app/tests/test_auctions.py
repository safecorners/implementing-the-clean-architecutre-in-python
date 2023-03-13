import logging

import factory
import injector
import pytest
from flask.testing import FlaskClient
from sqlalchemy.engine import Connection

from auctions import AuctionsRepository, BeginningAuction, BeginningAuctionInputDto
from auctions.domain.entities import Auction
from auctions.tests.factories import get_usd
from main.modules import RequestScope


class BeginningAuctionInputDtoFactory(factory.Factory):
    class Meta:
        model = BeginningAuctionInputDto

    auction_id = factory.Sequence(lambda n: n)
    title = factory.Faker("name")
    starting_price = get_usd("0.99")
    ends_at = factory.Faker("future_datetime", end_date="+7d")


@pytest.fixture()
def example_auction(container: injector.Injector) -> int:
    with container.get(RequestScope):
        beginning_auction_uc = container.get(BeginningAuction)
        dto = BeginningAuctionInputDtoFactory.build()
        logging.info(dto)
        beginning_auction_uc.execute(dto)
        auctions_repository = container.get(AuctionsRepository)
        auction = auctions_repository.get(dto.auction_id)
        logging.info(auction)
        connection = container.get(Connection)
        connection.commit()
        assert auction.id == dto.auction_id

    return int(dto.auction_id)


def test_single_auction(client: FlaskClient, example_auction: int) -> None:
    response = client.get(
        f"/auctions/{example_auction}", headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    logging.info(response.json)
    assert type(response.json) == dict


def test_returns_list_of_auctions(client: FlaskClient) -> None:
    response = client.get("/auctions/", headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert type(response.json) == list


@pytest.fixture()
def logged_in_client(client: FlaskClient) -> FlaskClient:
    email, password = "test+bid+1@cleanarchitecture.io", "password"
    client.post("/register", json={"email": email, "password": password})
    return client


def test_places_bid(example_auction: int, logged_in_client: FlaskClient) -> None:
    response = logged_in_client.post(
        f"/auctions/{example_auction}/bids", json={"amount": "15.99"}
    )

    assert response.status_code == 200
    assert response.json == {"message": "Hooray! You are a winner"}
