from typing import List

import pytz
from sqlalchemy.engine import Connection, Row

from auctions.application.repositories import AuctionsRepository
from auctions.domain.entities import Auction, Bid
from auctions.domain.value_objects import AuctionId
from auctions_infrastructure import auctions, bids
from foundation.events import EventBus
from foundation.value_objects.factories import get_usd


class SqlAlchemyAuctionsRepository(AuctionsRepository):
    def __init__(self, connection: Connection, event_bus: EventBus) -> None:
        self._conn = connection
        self._event_bus = event_bus

    def get(self, auction_id: AuctionId) -> Auction:
        row = self._conn.execute(
            auctions.select().where(auctions.c.id == auction_id)
        ).first()

        if not row:
            raise Exception("Not Found")

        bid_rows = self._conn.execute(
            bids.select().where(bids.c.auction_id == auction_id)
        ).fetchall()
        return self._row_to_entity(row, list(bid_rows))

    def _row_to_entity(self, auction_row: Row, bids_rows: List[Row]) -> Auction:
        auction_bids = [
            Bid(bid.id, bid.bidder_id, get_usd(bid.amount)) for bid in bids_rows
        ]
        return Auction(
            auction_row.id,
            auction_row.title,
            get_usd(auction_row.starting_price),
            auction_bids,
            auction_row.ends_at.replace(tzinfo=pytz.UTC),
            auction_row.ended,
        )

    def save(self, auction: Auction) -> None:
        raw_auction = {
            "title": auction.title,
            "starting_price": auction.starting_price.amount,
            "current_price": auction.current_price.amount,
            "ends_at": auction.ends_at,
            "ended": auction._ended,
        }
        update_result = self._conn.execute(
            auctions.update().where(auctions.c.id == auction.id).values(raw_auction)
        )
        if update_result.rowcount != 1:
            self._conn.execute(
                auctions.insert().values(dict(raw_auction, id=auction.id))
            )

        for bid in auction.bids:
            if bid.id:
                continue
            result = self._conn.execute(
                bids.insert().values(
                    {
                        "auction_id": auction.id,
                        "amount": bid.amount.amount,
                        "bidder_id": bid.bidder_id,
                    }
                )
            )
            (bid.id,) = result.inserted_primary_key

        if auction.withdrawn_bids_ids:
            self._conn.execute(
                bids.delete().where(bids.c.id.in_(auction.withdrawn_bids_ids))
            )

        for event in auction.domain_events:
            self._event_bus.post(event)

        auction.clear_events()
