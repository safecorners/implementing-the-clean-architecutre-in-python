import copy
from typing import Dict

from auctions.application.repositories import AuctionsRepository
from auctions.domain.entities import Auction
from auctions.domain.value_objects import AuctionId
from foundation.events import EventBus


class InMemoryAuctionsRepository(AuctionsRepository):
    def __init__(self, event_bus: EventBus) -> None:
        self._data: Dict[AuctionId, Auction] = {}
        self._event_bus = event_bus

    def get(self, auction_id: AuctionId) -> Auction:
        return copy.deepcopy(self._data[auction_id])

    def save(self, auction: Auction) -> None:
        for event in auction.domain_events:
            self._event_bus.post(event)
        auction.clear_events()
        self._data[auction.id] = copy.deepcopy(auction)
