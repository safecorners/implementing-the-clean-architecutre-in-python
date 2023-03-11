import injector

from auctions import Auctions
from main.module import AuctionsInfrastructure


def setup_dependency_injection() -> injector.Injector:
    return injector.Injector(
        [
            Auctions(),
            AuctionsInfrastructure(),
        ],
        auto_bind=False,
    )
