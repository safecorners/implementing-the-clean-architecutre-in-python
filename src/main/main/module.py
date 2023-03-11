import injector

from auctions import AuctionsRepository
from auctions.domain.entities import Auction
from auctions.domain.value_objects import Money
from auctions.domain.value_objects.money import currency
from auctions.tests.in_memory_repo import InMemoryAuctionsRepository


class AuctionsInfrastructure(injector.Module):
    @injector.provider
    def auctions_repository(self) -> AuctionsRepository:
        example_auction = Auction(
            id=1,
            title="examplary-auction",
            starting_price=Money(currency.USD, "12.99"),
            bids=[],
        )
        repository = InMemoryAuctionsRepository()
        repository.save(example_auction)
        return repository
