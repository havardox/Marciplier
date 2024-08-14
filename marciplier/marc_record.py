import json
from typing import Any

# Class representing the MARC21 Leader
class Leader:
    def __init__(self, value: str) -> None:
        self.value = value.strip('\n')

    def to_dict(self) -> dict[str, str]:
        return {
            "leader": f"{self.value}"
        }

    def __repr__(self) -> str:
        return f"Leader: {self.value}"


# Class representing a MARC21 subfield
class Subfield:
    def __init__(self, code: str, values: list[str]) -> None:
        self.code = code
        self.values = values

    def to_dict(self) -> dict[str, list[str]]:
        return {
            self.code: self.values
        }

    def __repr__(self) -> str:
        return f"Subfield(Code: {self.code}, Values: {self.values})"


# Base class for a generic MARC21 field
class Field:
    def __init__(self, tag: str, indicators: list[str] | None = None, subfields: list[Subfield] | None = None) -> None:
        self.tag = tag
        self.indicators = tuple(indicators) if indicators else ()
        self.subfields = subfields if subfields else []

    def add_subfield(self, code: str, value: str) -> None:
        # Check if subfield code already exists
        for subfield in self.subfields:
            if subfield.code == code:
                subfield.values.append(value)
                return
        # If code does not exist, create a new Subfield
        self.subfields.append(Subfield(code, [value]))

    def get_subfield(self, code: str) -> list[str]:
        subfields = []
        for subfield in self.subfields:
            if subfield.code == code:
                subfields.append(subfield)

        return subfields

    def to_dict(self) -> dict[str, Any]:
        subfields_list = [subfield.to_dict() for subfield in self.subfields]
        return {
            "indicators": self.indicators,
            "subfields": subfields_list
        }

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Indicators: {self.indicators}, Subfields: {self.subfields}"


# Derived class for control fields (00X fields)
class ControlField(Field):
    def __init__(self, tag: str, value: str) -> None:
        super().__init__(tag)
        self.value = value.strip('\n')

    def to_dict(self) -> dict[str, str]:
        return {
            self.tag: self.value
        }

    def __repr__(self) -> str:
        return f"ControlField(Tag: {self.tag}, Value: {self.value})"


# Derived class for data fields (01X-88X fields)
class DataField(Field):
    def __init__(self, tag: str, indicators: list[str] | None = None) -> None:
        super().__init__(tag, indicators)

    def __repr__(self) -> str:
        return f"DataField(Tag: {self.tag}, Indicators: {self.indicators}, Subfields: {self.subfields})"


# Class representing a MARC21 record
class MarcRecord:
    def __init__(self, leader: Leader) -> None:
        self.leader = leader
        self.controlfields: list[ControlField] = []
        self.datafields: list[DataField] = []

    def add_field(self, field: Field) -> None:
        if isinstance(field, ControlField):
            self.controlfields.append(field)
        elif isinstance(field, DataField):
            self.datafields.append(field)

    def get_field(self, tag: str) -> list[Field]:
        fields = []
        for field in self.controlfields:
            if field.tag == tag:
                fields.append(field)
        for field in self.datafields:
            if field.tag == tag:
                fields.append(field)
        return fields
    
    def to_dict(self) -> dict[str, Any]:
        record_dict = self.leader.to_dict()
        
        # Collect control fields
        controlfields_dict = {}
        for field in self.controlfields:
            controlfields_dict.update(field.to_dict())

        # Collect data fields
        datafields_dict = {}
        for field in self.datafields:
            tag = field.tag
            if tag not in datafields_dict:
                datafields_dict[tag] = []
            datafields_dict[tag].append(field.to_dict())

        if controlfields_dict:
            record_dict["controlfields"] = controlfields_dict
        if datafields_dict:
            record_dict["datafields"] = datafields_dict

        return record_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self) -> str:
        return f"MARC21Record(Leader: {self.leader}, ControlFields: {self.controlfields}, DataFields: {self.datafields})"
