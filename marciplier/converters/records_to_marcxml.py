import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from marciplier.marc_record import ControlField, DataField, MarcRecord

def records_to_marcxml(records: list[MarcRecord]) -> ET.Element:
    # Define the namespaces with the desired prefixes
    ns = {
        "marc": "http://www.loc.gov/MARC21/slim",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }

    # Register the namespaces to ensure the correct prefix is used
    for prefix, uri in ns.items():
        ET.register_namespace(prefix, uri)

    # Create the root element <marc:collection> with the additional attributes
    root = ET.Element(
        "{http://www.loc.gov/MARC21/slim}collection",
        {
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation":
            "http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"
        }
    )

    for record in records:
        record_elem = ET.SubElement(root, "{http://www.loc.gov/MARC21/slim}record")

        # Add leader element
        leader_elem = ET.SubElement(record_elem, "{http://www.loc.gov/MARC21/slim}leader")
        value = escape(record.leader.value)
        leader_elem.text = value

        # Add fields
        for field in record.controlfields:

            # Handle control fields
            control_field = ET.SubElement(
                record_elem, 
                "{http://www.loc.gov/MARC21/slim}controlfield", 
                tag=field.tag
            )
            control_field.text = escape(value)

        for field in record.datafields:
            # Handle data fields
            data_field = ET.SubElement(
                record_elem, 
                "{http://www.loc.gov/MARC21/slim}datafield", 
                tag=field.tag, 
                ind1=field.indicators[0] if field.indicators else " ", 
                ind2=field.indicators[1] if len(field.indicators) > 1 else " "
            )
            for subfield in field.subfields:
                for value in subfield.values:
                    subfield_elem = ET.SubElement(
                        data_field, 
                        "{http://www.loc.gov/MARC21/slim}subfield", 
                        code=subfield.code
                    )
                    subfield_elem.text = escape(value)


    return root
