from __future__ import annotations

from typing import List

from auctions.domain.entities.bid import Bid
from auctions.domain.value_objects import AuctionId, BidderId, BidId, Money


class Auction:
    def __init__(
        self,
        id: AuctionId,
        title: str,
        starting_price: Money,
        bids: List[Bid],
    ) -> None:
        self.id = id
        self.title = title
        self.starting_price = starting_price
        self.bids = sorted(bids, key=lambda bid: bid.amount)
        self._withdrawn_bids_ids: List[BidId] = []

    def place_bid(self, bidder_id: BidderId, amount: Money) -> None:
        if amount > self.starting_price:
            new_bid = Bid(
                id=None,
                bidder_id=bidder_id,
                amount=amount,
            )
            self.bids.append(new_bid)

    @property
    def current_price(self) -> Money:
        if not self.bids:
            return self.starting_price
        else:
            return self._highest_bid.amount

    @property
    def winners(self) -> List[BidderId]:
        if not self.bids:
            return []
        return [self._highest_bid.bidder_id]

    @property
    def _highest_bid(self) -> Bid:
        return self.bids[-1]

    def withdraw_bids(self, bids_ids: List[int]) -> None:
        self.bids = [bid for bid in self.bids if bid.id not in bids_ids]
        self._withdrawn_bids_ids.extend(bids_ids)

    @property
    def withdrawn_bids_ids(self) -> List[BidId]:
        return self._withdrawn_bids_ids

    def __str__(self) -> str:
        return f'<Auction #{self.id} title="{self.title}" current_price={self.current_price}>'

    def __eq__(self, other: Auction) -> bool:
        return isinstance(other, Auction) and vars(self) == vars(other)
