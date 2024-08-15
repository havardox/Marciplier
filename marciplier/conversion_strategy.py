# Strategy interface for conversion
from typing import Any, Protocol

from marciplier.marc_record import MarcRecord


class ConversionStrategy(Protocol):
    def to_records(self, src: Any) -> list[MarcRecord]:
        ...

    def from_records(self, src: list[MarcRecord]) -> Any:
        ...
