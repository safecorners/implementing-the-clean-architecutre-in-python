from auctions.domain.entities import Auction, Bid
from auctions.domain.value_objects.money import Money, currency
from auctions.tests.in_memory_repo import InMemoryAuctionsRepository


def test_should_get_back_saved_auction() -> None:
    bids = [Bid(id=1, bidder_id=1, amount=Money(currency.USD, "15.99"))]

    auction = Auction(
        id=1,
        title="awesome-book",
        starting_price=Money(currency.USD, "9.99"),
        bids=bids,
    )

    repository = InMemoryAuctionsRepository()

    repository.save(auction)

    assert repository.get(auction.id) == auction
