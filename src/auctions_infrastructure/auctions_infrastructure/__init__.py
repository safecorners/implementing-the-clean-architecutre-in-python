import injector
from sqlalchemy.engine import Connection

from auctions import AuctionsRepository, GetActiveAuctions, GetSingleAuction
from auctions_infrastructure.models import auctions, bids
from auctions_infrastructure.queries import SqlGetActiveAuctions, SqlGetSingleAuction
from auctions_infrastructure.repositories.auctions import SqlAlchemyAuctionsRepository

__all__ = [
    # module
    "AuctionsInfrastructure",
    # models
    "auctions",
    "bids",
]


class AuctionsInfrastructure(injector.Module):
    @injector.provider
    def get_active_auctions(self, conn: Connection) -> GetActiveAuctions:
        return SqlGetActiveAuctions(conn)

    @injector.provider
    def get_single_auction(self, conn: Connection) -> GetSingleAuction:
        return SqlGetSingleAuction(conn)

    @injector.provider
    def auctions_repository(self, conn: Connection) -> AuctionsRepository:
        return SqlAlchemyAuctionsRepository(conn)
