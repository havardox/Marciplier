import copy
import json
from marciplier.marc_record import MarcRecord


def records_to_json(records: list[MarcRecord], indent: str | int | None = None) -> list:
    converted = []
    for record in records:
        converted.append(record.to_dict())
    return json.dumps(converted, indent=indent)
