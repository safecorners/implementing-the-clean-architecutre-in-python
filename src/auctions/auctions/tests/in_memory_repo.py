import copy
from typing import Dict

from auctions.application.repositories import AuctionsRepository
from auctions.domain.entities import Auction
from auctions.domain.value_objects import AuctionId


class InMemoryAuctionsRepository(AuctionsRepository):
    def __init__(self) -> None:
        self._data: Dict[AuctionId, Auction] = {}

    def get(self, auction_id: AuctionId) -> Auction:
        return copy.deepcopy(self._data[auction_id])

    def save(self, auction: Auction) -> None:
        self._data[auction.id] = copy.deepcopy(auction)
