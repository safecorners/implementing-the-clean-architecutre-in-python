from dataclasses import dataclass
from typing import Optional
from auctions.domain.value_objects import BidId, BidderId, Money


@dataclass
class Bid:
    id: Optional[BidId]
    bidder_id: BidderId
    amount: Money
