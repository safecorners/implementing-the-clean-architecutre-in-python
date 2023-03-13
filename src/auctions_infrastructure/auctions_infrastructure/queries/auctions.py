import logging
from typing import List

from sqlalchemy import func
from sqlalchemy.engine import Row

from auctions.application.queries import AuctionDto, GetActiveAuctions, GetSingleAuction
from auctions.tests.factories import get_usd
from auctions_infrastructure import auctions
from auctions_infrastructure.queries.base import SqlQuery


class SqlGetActiveAuctions(GetActiveAuctions, SqlQuery):
    def query(self) -> List[AuctionDto]:
        return [
            _row_to_dto(row)
            for row in self._conn.execute(
                auctions.select().where(auctions.c.ends_at > func.now())
            )
        ]


class SqlGetSingleAuction(GetSingleAuction, SqlQuery):
    def query(self, auction_id: int) -> AuctionDto:
        logging.info(self._conn)
        logging.info(f"auction_id = {auction_id}")
        row = self._conn.execute(
            auctions.select().where(auctions.c.id == auction_id)
        ).first()
        logging.info(row)
        return _row_to_dto(row)


def _row_to_dto(auction_proxy: Row) -> AuctionDto:
    return AuctionDto(
        id=auction_proxy.id,
        title=auction_proxy.title,
        current_price=get_usd(auction_proxy.current_price),
        starting_price=get_usd(auction_proxy.starting_price),
        ends_at=auction_proxy.ends_at,
    )
