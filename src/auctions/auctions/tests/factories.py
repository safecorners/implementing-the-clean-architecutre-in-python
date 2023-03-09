from decimal import Decimal
from typing import Union

import factory

from auctions.domain.entities import Auction
from auctions.domain.value_objects.money import Money, currency


def get_usd(amount: Union[Decimal, str, float, int]) -> Money:
    return Money(currency.USD, amount)


class AuctionFactory(factory.Factory):
    class Meta:
        model = Auction

    id = factory.Sequence(lambda n: n)
    bids = factory.List([])
    title = factory.Faker("name")
    starting_price = get_usd("10.00")
