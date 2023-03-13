import os
from dataclasses import dataclass

import dotenv
import injector
from sqlalchemy.engine import Connection, Engine, create_engine

from auctions import Auctions
from auctions_infrastructure import AuctionsInfrastructure
from db_infrastructure import metadata
from main.modules import Db
from web_app_models import User

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
    settings = {}

    engine = create_engine(os.environ["DB_DSN"])
    dependency_injector = _setup_dependency_injection(settings, engine)
    _create_db_schema(engine)

    return AppContext(dependency_injector)


def _setup_dependency_injection(settings: dict, engine: Engine) -> injector.Injector:
    return injector.Injector(
        [
            Db(engine),
            Auctions(),
            AuctionsInfrastructure(),
        ],
        auto_bind=False,
    )


def _create_db_schema(engine: Engine) -> None:
    from auctions_infrastructure import auctions, bids  # noqa
    from web_app_models import Role, RolesUsers, User  # noqa

    metadata.create_all(engine)
