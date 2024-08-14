from collections import Counter
import json

from pymarc import Leader

from marciplier.marc_record import ControlField, DataField, MarcRecord

# Function to count unique fields and perform statistical analysis on field tags and tag-subfield pairs
def analyze_marc_records(marc_records: list[MarcRecord]) -> dict:
    unique_controlfields = set()
    unique_datafields = set()
    tag_subfield_counter = Counter()

    # Iterate over each MarcRecord
    for record in marc_records:
        # Count unique control fields and occurrences
        for field in record.controlfields:
            unique_controlfields.add(field.tag)
            tag_subfield_counter[field.tag] += 1

        # Count unique data fields with subfields and occurrences
        for field in record.datafields:
            for subfield in field.subfields:
                tag_subfield_pair = f"{field.tag}${subfield.code}"
                unique_datafields.add(tag_subfield_pair)
                tag_subfield_counter[tag_subfield_pair] += 1

    # Sort the dictionary by key
    sorted_tag_subfield_statistics = dict(sorted(tag_subfield_counter.items()))

    return {
        "unique_controlfields_count": len(unique_controlfields),
        "unique_datafields_with_subfields_count": len(unique_datafields),
        "tag_subfield_statistics": sorted_tag_subfield_statistics
    }
