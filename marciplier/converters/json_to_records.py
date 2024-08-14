from typing import Any, List, Dict
from marciplier.marc_record import ControlField, DataField, Leader, MarcRecord

def json_to_records(json_data: List[Dict[str, Any]]) -> List[MarcRecord]:
    records = []

    for record_dict in json_data:
        # Extract the leader
        leader_value = record_dict.get("leader", "")
        leader = Leader(leader_value)
        marc_record = MarcRecord(leader)

        # Process control fields
        controlfields = record_dict.get("controlfields", {})
        for tag, value in controlfields.items():
            control_field = ControlField(tag, value)
            marc_record.add_field(control_field)

        # Process data fields
        datafields = record_dict.get("datafields", {})
        for tag, content in datafields.items():
            for field_data in content:
                indicators = list(field_data.get("indicators", (" ", " ")))
                data_field = DataField(tag, indicators)

                for subfield_dict in field_data.get("subfields", []):
                    for code, values in subfield_dict.items():
                        if isinstance(values, list):
                            for value in values:
                                data_field.add_subfield(code, value)
                        else:
                            data_field.add_subfield(code, values)

                marc_record.add_field(data_field)

        # Add the fully constructed MarcRecord to the list of records
        records.append(marc_record)

    return records
