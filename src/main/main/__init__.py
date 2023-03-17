import os
from dataclasses import dataclass

import dotenv
import injector
from sqlalchemy.engine import Engine, create_engine

from auctions import Auctions
from auctions_infrastructure import AuctionsInfrastructure
from customer_relationship import CustomerRelationship
from db_infrastructure import metadata
from main.modules import Configs, Db, EventBusModule
from payments import Payments
from shipping import Shipping
from shipping_infrastructure import ShippingInfrastructure

__all__ = ["bootstrap_app"]


@dataclass
class AppContext:
    injector: injector.Injector


def bootstrap_app() -> AppContext:
    """
    This is bootstrap function independent from the context.
    This should be used for Web, CLI, or worker context.
    """
    config_path = os.environ.get(
        "CONFIG_PATH",
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, ".env_file"),
    )

    dotenv.load_dotenv(config_path)
    settings = {
        "payments.login": os.environ["PAYMENTS_LOGIN"],
        "payments.password": os.environ["PAYMENTS_PASSWORD"],
    }

    engine = create_engine(os.environ["DB_DSN"])
    dependency_injector = _setup_dependency_injection(settings, engine)
    _create_db_schema(engine)

    return AppContext(dependency_injector)


def _setup_dependency_injection(settings: dict, engine: Engine) -> injector.Injector:
    return injector.Injector(
        [
            Db(engine),
            Configs(settings),
            Auctions(),
            AuctionsInfrastructure(),
            CustomerRelationship(),
            EventBusModule(),
            Payments(),
            Shipping(),
            ShippingInfrastructure(),
        ],
        auto_bind=False,
    )


def _create_db_schema(engine: Engine) -> None:
    from auctions_infrastructure import auctions, bids  # noqa
    from web_app_models import Role, RolesUsers, User  # noqa

    metadata.create_all(engine)
