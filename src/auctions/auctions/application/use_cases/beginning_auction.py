from dataclasses import dataclass
from datetime import datetime

from auctions.application.repositories import AuctionsRepository
from auctions.domain.entities import Auction
from auctions.domain.exceptions import AuctionEndingInPast
from auctions.domain.value_objects import AuctionId, Money


@dataclass
class BeginningAuctionInputDto:
    auction_id: AuctionId
    title: str
    starting_price: Money
    ends_at: datetime


class BeginningAuction:
    def __init__(self, auctions_repository: AuctionsRepository) -> None:
        self.auctions_repository = auctions_repository

    def execute(self, input_dto: BeginningAuctionInputDto) -> None:
        if input_dto.ends_at < datetime.now(tz=input_dto.ends_at.tzinfo):
            raise AuctionEndingInPast

        auction = Auction.create(
            id=input_dto.auction_id,
            title=input_dto.title,
            starting_price=input_dto.starting_price,
            ends_at=input_dto.ends_at,
        )
        self.auctions_repository.save(auction)
