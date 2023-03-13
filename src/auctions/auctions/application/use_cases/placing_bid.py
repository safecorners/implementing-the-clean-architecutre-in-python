import abc
from dataclasses import dataclass

from auctions.application.repositories import AuctionsRepository
from auctions.domain.value_objects import AuctionId, BidderId, Money


@dataclass(frozen=True)
class PlacingBidInputDto:
    bidder_id: BidderId
    auction_id: AuctionId
    amount: Money


@dataclass(frozen=True)
class PlacingBidOutputDto:
    is_winner: bool
    current_price: Money


class PlacingBidOutputBoundary(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def present(self, output_dto: PlacingBidOutputDto) -> None:
        pass


class PlacingBid:
    def __init__(
        self,
        output_boundary: PlacingBidOutputBoundary,
        auctions_repository: AuctionsRepository,
    ) -> None:
        self._output_boundary = output_boundary
        self._auctions_repository = auctions_repository

    def execute(self, input_dto: PlacingBidInputDto) -> None:
        auction = self._auctions_repository.get(input_dto.auction_id)

        auction.place_bid(bidder_id=input_dto.bidder_id, amount=input_dto.amount)

        self._auctions_repository.save(auction)

        output_dto = PlacingBidOutputDto(
            is_winner=input_dto.bidder_id in auction.winners,
            current_price=auction.current_price,
        )

        self._output_boundary.present(output_dto)
