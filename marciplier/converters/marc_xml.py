# marcxml_to_records.py
import os
from typing import IO
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import xml.sax
import xml.sax.xmlreader
from dataclasses import dataclass, field

from marciplier.marc_record import (
    MarcRecord as ConvertedRecord,
    Leader as ConvertedLeader,
    ControlField as ConvertedControlField,
    DataField as ConvertedDataField,
)


# Custom exception to signal the parser to stop when the maximum number of records is reached
class FinishedParsing(Exception):
    pass


# Dataclass to manage the state while parsing MARC XML
@dataclass
class MarcXMLState:
    max_records: int | None = None  # Maximum number of records to parse
    current_marc_record: ConvertedRecord | None = None  # Current MARC record being parsed
    current_text: str | None = None  # Text content of the current XML element
    current_attrs: xml.sax.xmlreader.AttributesImpl | None = None  # Attributes of the current XML element
    current_open_tag: str | None = None  # Name of the current open tag in the XML
    current_record_count: int = 0  # Counter for records parsed
    finished: bool = False  # Flag to indicate if parsing should stop
    records: list = field(default_factory=list)  # List to store all parsed MARC records


# Base class for handling different MARC XML elements
class MarcXmlElement(object):
    DEFINED_EVENTS = ()  # Events this element class is interested in ("start", "end", etc.)

    def __init__(self, marc_xml_state: MarcXMLState) -> None:
        self.marc_xml_state = marc_xml_state

    def start(self):
        pass

    def end(self):
        pass

    def __str__(self):
        return "element"


# Class to handle the "record" element in the MARC XML
class Record(MarcXmlElement):
    DEFINED_EVENTS = (
        "start",
        "end",
    )

    def start(self):
        # Initialize a new MARC record
        self.marc_xml_state.current_marc_record = ConvertedRecord(
            leader=ConvertedLeader("")
        )
        # Check if the maximum record count has been reached
        if self.marc_xml_state.max_records is not None:
            self.marc_xml_state.current_record_count += 1
            if (
                self.marc_xml_state.current_record_count
                > self.marc_xml_state.max_records
            ):
                # Set the finished flag to stop further parsing
                self.marc_xml_state.finished = True

    def end(self):
        # Add the completed MARC record to the records list
        self.marc_xml_state.records.append(self.marc_xml_state.current_marc_record)


class Leader(MarcXmlElement):
    DEFINED_EVENTS = ("end",)

    def end(self):
        value = self.marc_xml_state.current_text
        # Set the leader in the current MARC record
        self.marc_xml_state.current_marc_record.leader.value = value


# Class to handle the "controlfield" element in the MARC XML
class ControlField(MarcXmlElement):
    DEFINED_EVENTS = ("end",)

    def end(self):
        tag = self.marc_xml_state.current_attrs.get("tag")
        value = self.marc_xml_state.current_text
        # Add a new control field to the current MARC record
        control_field = ConvertedControlField(tag=tag, values=[value])
        self.marc_xml_state.current_marc_record.add_field(control_field)


# Class to handle the "datafield" element in the MARC XML
class DataField(MarcXmlElement):
    DEFINED_EVENTS = ("start",)

    def start(self):
        # Store the tag of the current data field being parsed
        tag = self.marc_xml_state.current_attrs.get("tag")
        indicators = [
            self.marc_xml_state.current_attrs.get("ind1", " "),
            self.marc_xml_state.current_attrs.get("ind2", " "),
        ]
        # Add a new data field to the current MARC record
        data_field = ConvertedDataField(tag=tag, indicators=indicators)
        self.marc_xml_state.current_marc_record.add_field(data_field)
        self.marc_xml_state.current_open_tag = tag


# Class to handle the "subfield" element in the MARC XML
class Subfield(MarcXmlElement):
    DEFINED_EVENTS = ("end",)

    def end(self):
        tag = self.marc_xml_state.current_open_tag
        code = self.marc_xml_state.current_attrs.get("code")
        value = self.marc_xml_state.current_text

        # Find the last data field added and add a subfield to it
        for field in reversed(self.marc_xml_state.current_marc_record.data_fields):
            if isinstance(field, ConvertedDataField) and field.tag == tag:
                field.add_subfield(code=code, value=value)
                break


# XML SAX content handler for parsing MARC records
class MarcXmlHandler(xml.sax.handler.ContentHandler):
    def __init__(self, max_records: int | None = None):
        super().__init__()
        self.marc_xml_state = MarcXMLState(max_records=max_records)
        marc_element_classes = (
            Record,
            Leader,
            ControlField,
            DataField,
            Subfield,
        )  # Classes to handle different MARC elements
        self.current_line_count = 0  # Counter for the lines of text within an element
        self.elements_to_call = {
            "start": {},
            "end": {},
        }  # Dictionary to store handlers for start and end events

        # Initialize and store handlers for each MARC element
        for marc_element_class in marc_element_classes:
            marc_element = marc_element_class(marc_xml_state=self.marc_xml_state)
            element_name = marc_element_class.__name__.lower()
            if "start" in marc_element.DEFINED_EVENTS:
                self.elements_to_call["start"][element_name] = marc_element
            if "end" in marc_element.DEFINED_EVENTS:
                self.elements_to_call["end"][element_name] = marc_element

    # Handle the start of an XML element
    def startElement(self, name, attrs):
        local_name = name.split(":")[-1]
        marc_element = self.elements_to_call["start"].get(local_name)

        self.current_element = name
        self.marc_xml_state.current_attrs = attrs
        if marc_element is None:
            return
        marc_element.start()
        # If the parser has finished, raise an exception to stop parsing
        if self.marc_xml_state.finished:
            raise FinishedParsing

    # Handle the end of an XML element
    def endElement(self, name):
        local_name = name.split(":")[-1]
        self.current_line_count = 0
        marc_element = self.elements_to_call["end"].get(local_name)
        if marc_element is None:
            return
        marc_element.end()

    # Handle character data within an XML element
    def characters(self, content):
        if content.strip():
            if self.current_line_count > 0:
                # Append content to the existing text for multi-line elements
                self.marc_xml_state.current_text = (
                    self.marc_xml_state.current_text + content
                )
            else:
                self.current_line_count += 1
                # Set the text content for single-line elements
                self.marc_xml_state.current_text = content


class MarcXmlConversionStrategy:
    def to_records(self, src: str | os.PathLike | IO[bytes]) -> list[ConvertedRecord]:
        content_handler = MarcXmlHandler()

        try:
            # Parse the XML content from the provided source
            xml.sax.parse(src, content_handler)
        except FinishedParsing:
            pass

        return content_handler.marc_xml_state.records

    def from_records(self, src: list[ConvertedRecord]) -> ET.Element:

        # Define the namespaces with the desired prefixes
        ns = {
            "marc": "http://www.loc.gov/MARC21/slim",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }

        # Register the namespaces to ensure the correct prefix is used
        for prefix, uri in ns.items():
            ET.register_namespace(prefix, uri)

        # Create the root element <marc:collection> with the additional attributes
        root = ET.Element(
            "{http://www.loc.gov/MARC21/slim}collection",
            {
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"
            },
        )

        for record in src:
            record_elem = ET.SubElement(root, "{http://www.loc.gov/MARC21/slim}record")

            # Add leader element
            leader_elem = ET.SubElement(
                record_elem, "{http://www.loc.gov/MARC21/slim}leader"
            )
            value = escape(record.leader.value)
            leader_elem.text = value

            # Add fields
            for field in record.controlfields:

                # Handle control fields
                control_field = ET.SubElement(
                    record_elem,
                    "{http://www.loc.gov/MARC21/slim}controlfield",
                    tag=field.tag,
                )
                control_field.text = escape(value)

            for field in record.data_fields:
                # Handle data fields
                data_field = ET.SubElement(
                    record_elem,
                    "{http://www.loc.gov/MARC21/slim}datafield",
                    tag=field.tag,
                    ind1=field.indicators[0] if field.indicators else " ",
                    ind2=field.indicators[1] if len(field.indicators) > 1 else " ",
                )
                for subfield in field.subfields:
                    for value in subfield.values:
                        subfield_elem = ET.SubElement(
                            data_field,
                            "{http://www.loc.gov/MARC21/slim}subfield",
                            code=subfield.code,
                        )
                        subfield_elem.text = escape(value)

        return root
