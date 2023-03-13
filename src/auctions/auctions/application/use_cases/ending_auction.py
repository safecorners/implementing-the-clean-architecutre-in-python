from dataclasses import dataclass

from auctions.application.repositories import AuctionsRepository
from auctions.domain.value_objects import AuctionId


@dataclass(frozen=True)
class EndingAuctionInputDto:
    auction_id: AuctionId


class EndingAuction:
    def __init__(self, auctions_repo: AuctionsRepository) -> None:
        self._auctions_repo = auctions_repo

    def execute(self, input_dto: EndingAuctionInputDto) -> None:
        auction = self._auctions_repo.get(input_dto.auction_id)
        auction.end()
        # todo: payments
        self._auctions_repo.save(auction)
