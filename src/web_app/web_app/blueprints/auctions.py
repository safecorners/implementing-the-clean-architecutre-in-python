import flask_injector
import injector
from flask import Blueprint, Response, abort, jsonify, make_response, request
from flask_login import current_user

from auctions import (
    AuctionId,
    PlacingBid,
    PlacingBidInputDto,
    PlacingBidOutputBoundary,
    PlacingBidOutputDto,
)
from web_app.serialization.dto import get_dto

auctions_blueprint = Blueprint("auctions_blueprint", __name__)


class AuctionsWeb(injector.Module):
    @injector.provider
    @flask_injector.request
    def placing_bid_output_boundary(self) -> PlacingBidOutputBoundary:
        return PlacingBidPresenter()


@auctions_blueprint.route("/<int:auction_id>/bids", methods=["POST"])
def place_bid(
    auction_id: AuctionId,
    plcaing_bid_uc: PlacingBid,
    presenter: PlacingBidOutputBoundary,
) -> Response:
    if not current_user.is_authenticated:
        abort(403)

    dto = get_dto(
        request,
        PlacingBidInputDto,
        context={"auction_id": auction_id, "bidder_id": current_user.id},
    )
    plcaing_bid_uc.execute(dto)
    return presenter.response  # type: ignore


class PlacingBidPresenter(PlacingBidOutputBoundary):
    response: Response

    def present(self, output_dto: PlacingBidOutputDto) -> None:
        message = (
            "Hooray! You are a winner"
            if output_dto.is_winner
            else f"Your bid is too low. Current price is {output_dto.current_price}"
        )
        self.response = make_response(jsonify({"message": message}))
