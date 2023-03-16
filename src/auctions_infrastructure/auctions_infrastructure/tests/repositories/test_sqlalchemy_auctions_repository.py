from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from sqlalchemy import func, select
from sqlalchemy.engine import Connection, Engine, Row

from auctions.domain.entities import Auction, Bid
from auctions_infrastructure import auctions, bids
from auctions_infrastructure.repositories import SqlAlchemyAuctionsRepository
from db_infrastructure import Base
from foundation.events import Event, EventBus
from foundation.value_objects.factories import get_usd


@pytest.fixture
def event_bus_mock() -> Mock:
    return Mock(spec_set=EventBus)


class EventBusStub(EventBus):
    def __init__(self) -> None:
        self.events = []

    def emit(self, event: Event) -> None:
        self.events.append(event)


@pytest.fixture
def event_bus_stub() -> EventBusStub:
    return EventBusStub()


@pytest.fixture(scope="session")
def sqlalchemy_connect_url() -> str:
    return "sqlite:///:memory:"


@pytest.fixture(scope="session", autouse=True)
def setup_teardown_tables(engine: Engine) -> None:
    Base.metadata.create_all(engine)


@pytest.fixture()
def winning_bid_amount() -> Decimal:
    return Decimal("15.00")


@pytest.fixture()
def bidder_id(connection: Connection) -> int:
    return 1


@pytest.fixture()
def another_bidder_id() -> int:
    return 2


@pytest.fixture()
def expired_auction(connection: Connection, past_date: datetime) -> Row:
    connection.execute(
        auctions.insert().values(
            {
                "id": 0,
                "title": "Nothing interesting",
                "starting_price": Decimal("1.99"),
                "current_price": Decimal("1.99"),
                "ends_at": past_date,
                "ended": False,
            }
        )
    )
    return connection.execute(auctions.select().where(auctions.c.id == 0)).first()


@pytest.fixture()
def auction_model_with_a_bid(
    connection: Connection,
    winning_bid_amount: Decimal,
    bidder_id: int,
    ends_at: datetime,
) -> Row:
    connection.execute(
        auctions.insert().values(
            {
                "id": 1,
                "title": "Cool socks",
                "starting_price": winning_bid_amount / 2,
                "current_price": winning_bid_amount,
                "ends_at": ends_at,
                "ended": False,
            }
        )
    )
    connection.execute(
        bids.insert().values(
            {"amount": winning_bid_amount, "auction_id": 1, "bidder_id": bidder_id}
        )
    )
    return connection.execute(auctions.select().where(auctions.c.id == 1)).first()


@pytest.fixture()
def bid_model(connection: Connection, auction_model_with_a_bid: Row) -> Row:
    return connection.execute(
        bids.select().where(bids.c.auction_id == auction_model_with_a_bid.id)
    ).first()


@pytest.mark.usefixtures("transaction")
def test_gets_existing_auction(
    connection: Connection,
    auction_model_with_a_bid: Row,
    bid_model: Row,
    ends_at: datetime,
) -> None:
    auction = SqlAlchemyAuctionsRepository(connection).get(auction_model_with_a_bid.id)

    assert auction.id == auction_model_with_a_bid.id
    assert auction.title == auction_model_with_a_bid.title
    assert auction.starting_price == get_usd(auction_model_with_a_bid.starting_price)
    assert auction.current_price == get_usd(bid_model.amount)
    assert auction.ends_at == ends_at
    assert set(auction.bids) == {
        Bid(bid_model.id, bid_model.bidder_id, get_usd(bid_model.amount))
    }


@pytest.mark.usefixtures("transaction")
def test_saves_auction_changes(
    connection: Connection,
    another_bidder_id: int,
    bid_model: Row,
    auction_model_with_a_bid: Row,
    ends_at: datetime,
) -> None:
    new_bid_price = get_usd(bid_model.amount * 2)
    auction = Auction(
        id=auction_model_with_a_bid.id,
        title=auction_model_with_a_bid.title,
        starting_price=get_usd(auction_model_with_a_bid.starting_price),
        ends_at=ends_at,
        bids=[
            Bid(bid_model.id, bid_model.bidder_id, get_usd(bid_model.amount)),
            Bid(None, another_bidder_id, new_bid_price),
        ],
        ended=True,
    )

    SqlAlchemyAuctionsRepository(connection).save(auction)
    assert connection.execute(select(func.count("*")).select_from(bids)).scalar() == 2
    saved_auction = connection.execute(
        select(auctions).where(auctions.c.id == auction_model_with_a_bid.id)
    ).first()
    assert saved_auction.current_price == new_bid_price.amount
    assert saved_auction.ended


@pytest.mark.usefixtures("transaction")
def test_removes_withdrawn_bids(
    connection: Connection,
    bid_model: Row,
    auction_model_with_a_bid: dict,
    ends_at: datetime,
) -> None:
    auction = Auction(
        id=auction_model_with_a_bid.id,
        title=auction_model_with_a_bid.title,
        starting_price=get_usd(auction_model_with_a_bid.starting_price),
        ends_at=ends_at,
        bids=[Bid(bid_model.id, bid_model.bidder_id, get_usd(bid_model.amount))],
        ended=False,
    )
    auction.withdraw_bids([bid_model.id])

    SqlAlchemyAuctionsRepository(connection).save(auction)

    assert connection.execute(select(func.count()).select_from(bids)).scalar() == 0
