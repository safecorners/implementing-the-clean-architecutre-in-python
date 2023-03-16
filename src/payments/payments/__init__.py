import injector
from sqlalchemy.engine import Connection

from payments.config import PaymentsConfig
from payments.facade import PaymentsFacade

__all__ = [
    # module
    "Payments",
    "PaymentsConfig",
    # facade
    "PaymentsFacade",
]


class Payments(injector.Module):
    @injector.provider
    def facade(self, config: PaymentsConfig, connection: Connection) -> PaymentsFacade:
        return PaymentsFacade(config, connection)
