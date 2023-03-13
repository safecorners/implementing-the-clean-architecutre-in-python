from datetime import datetime, timedelta
from typing import Optional

import pytest
import pytz
from freezegun import freeze_time

from auctions import BeginningAuction, PlacingBid
from auctions.application.repositories import AuctionsRepository
from auctions.application.use_cases.beginning_auction import BeginningAuctionInputDto
from auctions.application.use_cases.placing_bid import (
    PlacingBidInputDto,
    PlacingBidOutputBoundary,
    PlacingBidOutputDto,
)
from auctions.domain.entities import Auction
from auctions.domain.exceptions import BidOnEndedAuction
from auctions.domain.value_objects import AuctionId
from auctions.tests.factories import AuctionFactory, get_usd
from auctions.tests.in_memory_repo import InMemoryAuctionsRepository


class PlacingBidOutputBoundaryFake(PlacingBidOutputBoundary):
    def __init__(self) -> None:
        self.dto: Optional[PlacingBidOutputDto] = None

    def present(self, output_dto: PlacingBidOutputDto) -> None:
        self.dto = output_dto


@pytest.fixture()
def output_boundary() -> PlacingBidOutputBoundary:
    return PlacingBidOutputBoundaryFake()


@pytest.fixture()
def auction() -> Auction:
    return AuctionFactory()


@pytest.fixture()
def auction_id(auction: Auction) -> AuctionId:
    return auction.id


@pytest.fixture()
def auction_title(auction: Auction) -> str:
    return auction.title


@pytest.fixture()
def auctions_repo() -> AuctionsRepository:
    return InMemoryAuctionsRepository()


@pytest.fixture()
def place_bid_uc(
    output_boundary: PlacingBidOutputBoundaryFake,
    auction: Auction,
    auctions_repo: AuctionsRepository,
) -> PlacingBid:
    auctions_repo.save(auction)
    return PlacingBid(output_boundary, auctions_repo)


@pytest.fixture()
def beginning_auction_uc(auctions_repo: AuctionsRepository) -> BeginningAuction:
    return BeginningAuction(auctions_repo)


def test_Auction_FirstBidHigherThanInitialPrice_IsWinning(
    place_bid_uc: PlacingBid,
    output_boundary: PlacingBidOutputBoundaryFake,
    auction_id: AuctionId,
) -> None:
    place_bid_uc.execute(PlacingBidInputDto(1, auction_id, get_usd("100")))

    expected_dto = PlacingBidOutputDto(is_winner=True, current_price=get_usd("100"))

    assert output_boundary.dto == expected_dto


def test_Auction_BidLowerThanCurrentPrice_IsLosing(
    place_bid_uc: PlacingBid,
    output_boundary: PlacingBidOutputBoundaryFake,
    auction_id: AuctionId,
) -> None:
    place_bid_uc.execute(PlacingBidInputDto(1, auction_id, get_usd("5")))

    assert output_boundary.dto == PlacingBidOutputDto(
        is_winner=False, current_price=get_usd("10")
    )


def test_Auction_Overbid_IsWinning(
    place_bid_uc: PlacingBid,
    output_boundary: PlacingBidOutputBoundaryFake,
    auction_id: AuctionId,
) -> None:
    place_bid_uc.execute(PlacingBidInputDto(1, auction_id, get_usd("100")))

    place_bid_uc.execute(PlacingBidInputDto(2, auction_id, get_usd("120")))

    assert output_boundary.dto == PlacingBidOutputDto(
        is_winner=True, current_price=get_usd("120")
    )


def test_Auction_OverbidByWinner_IsWinning(
    place_bid_uc: PlacingBid,
    output_boundary: PlacingBidOutputBoundaryFake,
    auction_id: AuctionId,
) -> None:
    place_bid_uc.execute(PlacingBidInputDto(1, auction_id, get_usd("100")))

    place_bid_uc.execute(PlacingBidInputDto(1, auction_id, get_usd("120")))

    assert output_boundary.dto == PlacingBidOutputDto(
        is_winner=True, current_price=get_usd("120")
    )


def test_bid_on_ended_auction_raises_exception(
    beginning_auction_uc: BeginningAuction, place_bid_uc: PlacingBid
) -> None:
    yesterday = datetime.now() - timedelta(days=1)

    with freeze_time(yesterday):
        beginning_auction_uc.execute(
            BeginningAuctionInputDto(
                1, "Bar", get_usd("1.00"), yesterday + timedelta(hours=1)
            )
        )

    with pytest.raises(BidOnEndedAuction):
        place_bid_uc.execute(
            PlacingBidInputDto(bidder_id=1, auction_id=1, amount=get_usd("2.00"))
        )
