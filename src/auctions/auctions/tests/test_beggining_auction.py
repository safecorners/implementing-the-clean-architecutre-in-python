from datetime import datetime, timedelta

import pytest

from auctions.application.use_cases import BeginningAuction, BeginningAuctionInputDto
from auctions.domain.exceptions import AuctionEndingInPast
from auctions.tests.in_memory_repo import InMemoryAuctionsRepository
from foundation.value_objects.factories import get_usd


@pytest.fixture()
def repo() -> InMemoryAuctionsRepository:
    return InMemoryAuctionsRepository()


@pytest.fixture()
def beginning_auction_uc(repo: InMemoryAuctionsRepository) -> BeginningAuction:
    return BeginningAuction(repo)


def test_BeginningAuction_BeforeEndDate(
    beginning_auction_uc: BeginningAuction, repo: InMemoryAuctionsRepository
) -> None:
    input_dto = BeginningAuctionInputDto(
        1, "bar-auction", get_usd("2.00"), datetime.now() + timedelta(days=7)
    )
    beginning_auction_uc.execute(input_dto)

    assert repo.get(1)


def test_BeginningAuction_EndsAtInThePast_raisesException(
    beginning_auction_uc: BeginningAuction,
) -> None:
    yesterday = datetime.now() - timedelta(days=1)
    with pytest.raises(AuctionEndingInPast):
        beginning_auction_uc.execute(
            BeginningAuctionInputDto(1, "foo-auction", get_usd("1.00"), yesterday)
        )
