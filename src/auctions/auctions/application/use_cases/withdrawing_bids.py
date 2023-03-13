from dataclasses import dataclass
from typing import List

from auctions.application.repositories import AuctionsRepository
from auctions.domain.value_objects import AuctionId, BidId


@dataclass
class WithdrawingBidsInputDto:
    auction_id: AuctionId
    bids_ids: List[BidId]


class WithdrawingBids:
    def __init__(self, auctions_repository: AuctionsRepository) -> None:
        self._auctions_repository = auctions_repository

    def execute(self, input_dto: WithdrawingBidsInputDto) -> None:
        auction = self._auctions_repository.get(input_dto.auction_id)
        auction.withdraw_bids(input_dto.bids_ids)
        self._auctions_repository.save(auction)
