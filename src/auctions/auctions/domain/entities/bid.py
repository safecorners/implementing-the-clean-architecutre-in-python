from dataclasses import dataclass
from typing import Optional

from auctions.domain.value_objects import BidderId, BidId
from foundation.value_objects import Money


@dataclass(unsafe_hash=True)
class Bid:
    id: Optional[BidId]
    bidder_id: BidderId
    amount: Money
