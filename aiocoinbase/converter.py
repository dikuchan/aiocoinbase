from contextlib import suppress
from datetime import datetime
from decimal import Decimal
from typing import Type

import cattrs
import ciso8601


class Converter(cattrs.GenConverter):
    def __init__(self) -> None:
        super().__init__()

        # Convert decimal.
        self.register_structure_hook(Decimal, self._structure_decimal)
        self.register_unstructure_hook(Decimal, self._unstructure_decimal)
        # Convert Coinbase time to datetime.
        self.register_structure_hook(datetime, self._structure_datetime)
        self.register_unstructure_hook(datetime, self._unstructure_datetime)

    @staticmethod
    def _structure_decimal(obj: str, _: Type[Decimal]) -> Decimal:
        return Decimal(obj)

    @staticmethod
    def _unstructure_decimal(obj: Decimal) -> str:
        return str(obj)

    @staticmethod
    def _structure_datetime(obj: str, _: Type[datetime]) -> datetime:
        with suppress(ValueError, TypeError):
            return ciso8601.parse_datetime(obj)
        raise ValueError

    @staticmethod
    def _unstructure_datetime(obj: datetime) -> int:
        return int(1000 * obj.timestamp())
