from dataclasses import dataclass
from uuid import UUID


@dataclass
class ShippingPackageInputDto:
    package_uuid: UUID


class ShippingPackage:
    ...
