import injector

__all__ = [
    # module
    "Auctions",
    # value objects
    "AuctionId",
    # repositories
    "AuctionsRepository",
    # use cases
    "PlacingBid",
    "WithdrawingBids",
    # input dtos
    "PlacingBidInputDto",
    "WithdrawingBidsInputDto",
    # output dtos
    "PlacingBidOutputDto",
    # boundary
    "PlacingBidOutputBoundary",
]

from auctions.application.repositories import AuctionsRepository
from auctions.application.use_cases import (
    PlacingBid,
    PlacingBidInputDto,
    PlacingBidOutputBoundary,
    PlacingBidOutputDto,
    WithdrawingBids,
    WithdrawingBidsInputDto,
)
from auctions.domain.value_objects import AuctionId


class Auctions(injector.Module):
    @injector.provider
    def placing_bid_uc(
        self, boundary: PlacingBidOutputBoundary, repo: AuctionsRepository
    ) -> PlacingBid:
        return PlacingBid(boundary, repo)

    @injector.provider
    def Withdrawing_bids_uc(self, repo: AuctionsRepository) -> WithdrawingBids:
        return WithdrawingBids(repo)
