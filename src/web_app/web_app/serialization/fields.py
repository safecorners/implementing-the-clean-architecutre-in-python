from __future__ import annotations

import typing

from marshmallow import exceptions, fields

from auctions.domain.value_objects import Money
from auctions.tests.factories import get_usd


class Dollars(fields.Field):
    def _serialize(
        self, value: typing.Any, attr: str | None, obj: typing.Any, **kwargs: object
    ) -> str:
        return str(value)

    def _deserialize(
        self,
        value: typing.Any,
        attr: str | None,
        data: typing.Mapping[str, typing.Any] | None,
        **kwargs: object,
    ) -> Money:
        try:
            return get_usd(value)
        except ValueError as exc:
            raise exceptions.ValidationError(str(exc))
