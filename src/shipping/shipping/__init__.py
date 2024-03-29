import injector

from shipping.application.queries import GetNextPackage, PackageDto
from shipping.application.repositories import AddressRepository
from shipping.application.use_cases import ShippingPackage, ShippingPackageInputDto

__all__ = [
    # module
    "Shipping",
    # events
    # repositories
    "AddressRepository",
    # use cases
    "ShippingPackage",
    "ShippingPackageInputDto",
    # queries
    "GetNextPackage",
    "PackageDto",
]


class Shipping(injector.Module):
    ...
