import logging

import factory
import injector
import pytest
from flask.testing import FlaskClient

from auctions.application.repositories import AuctionsRepository
from auctions.domain.entities import Auction
from auctions.tests.factories import AuctionFactory, get_usd
from main.modules import RequestScope


@pytest.fixture()
def example_auction(container: injector.Injector) -> int:
    with container.get(RequestScope):
        auctions_repository = container.get(AuctionsRepository)
        auction: Auction = AuctionFactory.build()
        auctions_repository.save(auction)
        logging.info(auction)

    return int(auction.id)


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
