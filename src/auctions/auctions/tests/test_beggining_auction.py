from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from auctions.application.use_cases import BeginningAuction, BeginningAuctionInputDto
from auctions.domain.events import AuctionBegan
from auctions.domain.exceptions import AuctionEndingInPast
from auctions.tests.in_memory_repo import InMemoryAuctionsRepository
from foundation.events import EventBus
from foundation.value_objects.factories import get_usd


@pytest.fixture()
def event_bus_mock() -> Mock:
    return Mock(spec_set=EventBus)


@pytest.fixture()
def repo(event_bus_mock: Mock) -> InMemoryAuctionsRepository:
    return InMemoryAuctionsRepository(event_bus_mock)


@pytest.fixture()
def beginning_auction_uc(repo: InMemoryAuctionsRepository) -> BeginningAuction:
    return BeginningAuction(repo)


def test_BeginningAuction_BeforeEndDate_emitsEvent(
    beginning_auction_uc: BeginningAuction, event_bus_mock: Mock
) -> None:
    input_dto = BeginningAuctionInputDto(
        1, "bar-auction", get_usd("2.00"), datetime.now() + timedelta(days=7)
    )
    beginning_auction_uc.execute(input_dto)

    event_bus_mock.emit.assert_called_once_with(
        AuctionBegan(1, get_usd("2.00"), "bar-auction")
    )


def test_BeginningAuction_EndsAtInThePast_raisesException(
    beginning_auction_uc: BeginningAuction,
) -> None:
    yesterday = datetime.now() - timedelta(days=1)
    with pytest.raises(AuctionEndingInPast):
        beginning_auction_uc.execute(
            BeginningAuctionInputDto(1, "foo-auction", get_usd("1.00"), yesterday)
        )
