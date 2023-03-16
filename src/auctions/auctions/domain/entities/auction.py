from __future__ import annotations

from datetime import datetime
from typing import List

from auctions.domain.entities.bid import Bid
from auctions.domain.exceptions import (
    AuctionAlreadyEnded,
    AuctionHasNotEnded,
    BidOnEndedAuction,
)
from auctions.domain.value_objects import AuctionId, BidderId, BidId
from foundation.value_objects import Money


class Auction:
    def __init__(
        self,
        id: AuctionId,
        title: str,
        starting_price: Money,
        bids: List[Bid],
        ends_at: datetime,
        ended: bool,
    ) -> None:
        self.id = id
        self.title = title
        self.starting_price = starting_price
        self.bids = sorted(bids, key=lambda bid: bid.amount)
        self.ends_at = ends_at
        self._ended = ended
        self._withdrawn_bids_ids: List[BidId] = []

    def place_bid(self, bidder_id: BidderId, amount: Money) -> None:
        if self._should_end:
            raise BidOnEndedAuction

        if amount > self.starting_price:
            new_bid = Bid(
                id=None,
                bidder_id=bidder_id,
                amount=amount,
            )
            self.bids.append(new_bid)

    @property
    def _should_end(self) -> bool:
        return datetime.now(tz=self.ends_at.tzinfo) > self.ends_at

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

    def end(self) -> None:
        if not self._should_end:
            raise AuctionHasNotEnded
        if self._ended is True:
            raise AuctionAlreadyEnded

        self._ended = True

    @classmethod
    def create(
        cls, id: AuctionId, title: str, starting_price: Money, ends_at: datetime
    ) -> Auction:
        auction = Auction(
            id=id,
            title=title,
            starting_price=starting_price,
            bids=[],
            ends_at=ends_at,
            ended=False,
        )
        return auction

    def __str__(self) -> str:
        return f'<Auction #{self.id} title="{self.title}" current_price={self.current_price}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Auction) and vars(self) == vars(other)
