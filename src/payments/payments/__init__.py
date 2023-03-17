import injector
from sqlalchemy.engine import Connection

from foundation.events import EventBus
from payments.config import PaymentsConfig
from payments.events import (
    PaymentCaptured,
    PaymentCharged,
    PaymentFailed,
    PaymentStarted,
)
from payments.facade import PaymentsFacade

__all__ = [
    # module
    "Payments",
    "PaymentsConfig",
    # facade
    "PaymentsFacade",
    # events
    "PaymentStarted",
    "PaymentCharged",
    "PaymentCaptured",
    "PaymentFailed",
]


class Payments(injector.Module):
    @injector.provider
    def facade(
        self, config: PaymentsConfig, connection: Connection, event_bus: EventBus
    ) -> PaymentsFacade:
        return PaymentsFacade(config, connection, event_bus)
