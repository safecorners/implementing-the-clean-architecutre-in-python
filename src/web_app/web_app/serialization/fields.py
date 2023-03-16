from __future__ import annotations

import typing

from foundation.value_objects import Money
from foundation.value_objects.factories import get_usd
from marshmallow import exceptions, fields


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
