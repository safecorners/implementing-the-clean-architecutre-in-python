import injector
from sqlalchemy.engine import Connection

from customer_relationship.config import CustomerRelationshipConfig
from customer_relationship.facade import CustomerRelationshipFacade
from customer_relationship.models import customers

__all__ = [
    # module
    "CustomerRelationship",
    "CustomerRelationshipConfig",
    # facade
    "CustomerRelationshipFacade",
    # models
    "customers",
]


class CustomerRelationship(injector.Module):
    @injector.provider
    def facade(
        self, config: CustomerRelationshipConfig, connection: Connection
    ) -> CustomerRelationshipFacade:
        return CustomerRelationshipFacade(config, connection)
