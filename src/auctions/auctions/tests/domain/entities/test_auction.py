from datetime import datetime, timedelta

import pytest

from auctions.domain.entities import Bid
from auctions.domain.exceptions import (
    AuctionAlreadyEnded,
    AuctionHasNotEnded,
    BidOnEndedAuction,
)
from auctions.tests.factories import AuctionFactory
from foundation.value_objects.factories import get_usd


@pytest.fixture()
def yesterday() -> datetime:
    return datetime.now() - timedelta(days=1)


def test_should_use_starting_price_as_current_price_for_empty_bids_list() -> None:
    auction = AuctionFactory()

    assert auction.current_price == auction.starting_price


def test_should_return_highest_bid_for_current_price() -> None:
    auction = AuctionFactory(
        bids=[
            Bid(id=1, bidder_id=1, amount=get_usd("20")),
            Bid(id=2, bidder_id=2, amount=get_usd("15")),
        ]
    )

    assert auction.current_price == get_usd("20")


def test_should_return_no_winners_for_empty_bids_list() -> None:
    auction = AuctionFactory()

    assert auction.winners == []


def test_should_return_highest_bids_user_id_for_winners_list() -> None:
    auction = AuctionFactory(
        bids=[
            Bid(id=1, bidder_id=1, amount=get_usd("101")),
            Bid(id=2, bidder_id=2, amount=get_usd("15")),
            Bid(id=3, bidder_id=3, amount=get_usd("100")),
        ]
    )

    assert auction.winners == [1]


def test_should_win_auction_if_is_the_only_bidder_above_starting_price() -> None:
    auction = AuctionFactory()

    auction.place_bid(bidder_id=1, amount=get_usd("11"))

    assert auction.winners == [1]


def test_should_not_be_winning_auction_if_bids_below_starting_price() -> None:
    auction = AuctionFactory(starting_price=get_usd("10.00"))

    auction.place_bid(bidder_id=1, amount=get_usd("5"))

    assert auction.winners == []


def test_should_withdraw_the_only_bid() -> None:
    auction = AuctionFactory(bids=[Bid(id=1, bidder_id=1, amount=get_usd("50"))])

    auction.withdraw_bids([1])

    assert auction.winners == []
    assert auction.current_price == auction.starting_price


def test_should_add_withdrawn_bids_ids_to_seperate_list() -> None:
    auction = AuctionFactory(bids=[Bid(id=1, bidder_id=1, amount=get_usd("50"))])

    auction.withdraw_bids([1])

    assert auction.withdrawn_bids_ids == [1]


def test_should_not_be_winning_if_bid_lower_than_current_price() -> None:
    auction = AuctionFactory(bids=[Bid(id=1, bidder_id=1, amount=get_usd("10.00"))])

    lower_bid_bidder_id = 2
    auction.place_bid(bidder_id=lower_bid_bidder_id, amount=get_usd("5.00"))

    assert lower_bid_bidder_id not in auction.winners


def test_should_not_allow_placing_bids_for_ended_auction(yesterday: datetime) -> None:
    auction = AuctionFactory(ends_at=yesterday)

    with pytest.raises(BidOnEndedAuction):
        auction.place_bid(bidder_id=1, amount=auction.current_price + get_usd("1.00"))


def test_should_raise_if_auction_has_not_been_ended() -> None:
    auction = AuctionFactory()

    with pytest.raises(AuctionHasNotEnded):
        auction.end()


def test_EndedAuction_PlacingBid_RaisesException(yesterday: datetime) -> None:
    auction = AuctionFactory(ends_at=yesterday)
    auction.end()

    with pytest.raises(BidOnEndedAuction):
        auction.place_bid(bidder_id=1, amount=get_usd("19.99"))


def test_EndedAuction_Ending_RaisesException(yesterday: datetime) -> None:
    auction = AuctionFactory(ends_at=yesterday)
    auction.end()

    with pytest.raises(AuctionAlreadyEnded):
        auction.end()
