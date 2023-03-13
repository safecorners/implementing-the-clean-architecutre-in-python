import json
from datetime import datetime
from functools import singledispatchmethod

from auctions import AuctionDto
from auctions.domain.value_objects import Money


class JSONEncoder(json.JSONEncoder):
    @singledispatchmethod
    def default(self, o: object) -> object:
        raise TypeError(f"Cannot serialize {type(o)}")

    @default.register(AuctionDto)
    def serialize_auction_dto(self, obj: AuctionDto) -> object:
        return {
            "id": obj.id,
            "title": obj.title,
            "current_price": obj.current_price,
            "starting_price:": obj.starting_price,
        }

    @default.register(Money)
    def serialize_money(self, obj: Money) -> object:
        return {"amount": str(obj.amount), "currency": obj.currency.iso_code}

    @default.register(datetime)
    def serialize_datetime(self, obj: datetime) -> str:
        return obj.isoformat()
