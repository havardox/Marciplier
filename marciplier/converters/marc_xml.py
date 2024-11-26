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

class FinishedParsing(Exception):
    """Signals the parser to stop when the maximum number of records is reached."""
    pass

@dataclass
class MarcXMLState:
    """Manages the state while parsing MARC XML."""
    max_records: int = None # Maximum number of records to parse
    current_marc_record: ConvertedRecord | None = None # Current MARC record being parsed
    current_text: str | None = None # Text content of the current XML element
    current_attrs: xml.sax.xmlreader.AttributesImpl = None # Attributes of the current XML element
    current_open_tag: str = None # Name of the current open tag in the XML
    current_record_count: int = 0 # Counter for number of records parsed
    finished: bool = False  # Flag to indicate if parsing should stop
    records: list = field(default_factory=list) # List to store all parsed MARC records

class MarcXmlElement:
    """Base class for handling MARC XML elements."""
    DEFINED_EVENTS = ()

# Base class for handling different MARC XML elements
class MarcXmlElement(object):
    DEFINED_EVENTS = ()  # Events this element class is interested in ("start" or "end")

    def __init__(self, marc_xml_state: MarcXMLState) -> None:
        self.marc_xml_state = marc_xml_state

    def start(self):
        """Handles actions at the start of the element."""
        pass

    def end(self):
        """Handles actions at the end of the element."""
        pass

    def __str__(self):
        return "element"

class Record(MarcXmlElement):
    """Handles the 'record' element in MARC XML."""
    DEFINED_EVENTS = ("start", "end")

    def start(self):
        """Initializes a new MARC record and checks record count."""
        self.marc_xml_state.current_marc_record = ConvertedRecord(
            leader=ConvertedLeader("")
        )
         # Check if the maximum record count has been reached
        if self.marc_xml_state.max_records is not None:
            self.marc_xml_state.current_record_count += 1
            if self.marc_xml_state.current_record_count > self.marc_xml_state.max_records:
                # Set the finished flag to stop further parsing
                self.marc_xml_state.finished = True

    def end(self):
        """Adds the completed MARC record to the records list."""
        self.marc_xml_state.records.append(self.marc_xml_state.current_marc_record)

class Leader(MarcXmlElement):
    """Handles the 'leader' element in MARC XML."""
    DEFINED_EVENTS = ("end",)

    def end(self):
        """Sets the leader in the current MARC record."""
        value = self.marc_xml_state.current_text

        # Set the leader in the current MARC record
        self.marc_xml_state.current_marc_record.leader.value = value

class ControlField(MarcXmlElement):
    """Handles the 'controlfield' element in MARC XML."""
    DEFINED_EVENTS = ("end",)

    def end(self):
        """Adds a control field to the current MARC record."""
        tag = self.marc_xml_state.current_attrs.get("tag")
        value = self.marc_xml_state.current_text

        # Add a new control field to the current MARC record
        control_field = ConvertedControlField(tag=tag, values=[value])
        self.marc_xml_state.current_marc_record.add_field(control_field)

class DataField(MarcXmlElement):
    """Handles the 'datafield' element in MARC XML."""
    DEFINED_EVENTS = ("start",)

    def start(self):
        """Adds a data field to the current MARC record."""
        tag = self.marc_xml_state.current_attrs.get("tag")
        indicators = [
            self.marc_xml_state.current_attrs.get("ind1", " "),
            self.marc_xml_state.current_attrs.get("ind2", " "),
        ]

        # Add a new data field to the current MARC record
        data_field = ConvertedDataField(tag=tag, indicators=indicators)
        self.marc_xml_state.current_marc_record.add_field(data_field)
        self.marc_xml_state.current_open_tag = tag

class Subfield(MarcXmlElement):
    """Handles the 'subfield' element in MARC XML."""
    DEFINED_EVENTS = ("end",)

    def end(self):
        """Adds a subfield to the last data field in the current MARC record."""
        tag = self.marc_xml_state.current_open_tag
        code = self.marc_xml_state.current_attrs.get("code")
        value = self.marc_xml_state.current_text

        # Find the last data field added and add a subfield to it
        for field in reversed(self.marc_xml_state.current_marc_record.data_fields):
            if isinstance(field, ConvertedDataField) and field.tag == tag:
                field.add_subfield(code=code, value=value)
                break

class MarcXmlHandler(xml.sax.handler.ContentHandler):
    """XML SAX content handler for parsing MARC records."""

    def __init__(self, max_records=None):
        """
        Initializes the handler with a maximum record count and element handlers.

        Args:
            max_records: Maximum number of records to parse.
        """
        super().__init__()
        self.marc_xml_state = MarcXMLState(max_records=max_records)
        self.current_line_count = 0
        # Dictionary to store handlers for start and end events
        self.elements_to_call = {"start": {}, "end": {}}

        # Classes to handle different MARC elements
        marc_element_classes = (Record, Leader, ControlField, DataField, Subfield) 

        # Initialize and store handlers for each MARC element
        for marc_element_class in marc_element_classes:
            marc_element = marc_element_class(marc_xml_state=self.marc_xml_state)
            element_name = marc_element_class.__name__.lower()
            if "start" in marc_element.DEFINED_EVENTS:
                self.elements_to_call["start"][element_name] = marc_element
            if "end" in marc_element.DEFINED_EVENTS:
                self.elements_to_call["end"][element_name] = marc_element

    def startElement(self, name, attrs):
        """
        Handles the start of an XML element.

        Args:
            name: Name of the XML element.
            attrs: Attributes of the XML element.
        """
        local_name = name.split(":")[-1]
        marc_element = self.elements_to_call["start"].get(local_name)

        self.current_element = name
        self.marc_xml_state.current_attrs = attrs
        if marc_element is not None:
            marc_element.start()
            # If the parser has finished, raise an exception to stop parsing
            if self.marc_xml_state.finished:
                raise FinishedParsing

    def endElement(self, name):
        """
        Handles the end of an XML element.

        Args:
            name: Name of the XML element.
        """
        local_name = name.split(":")[-1]
        self.current_line_count = 0
        marc_element = self.elements_to_call["end"].get(local_name)
        if marc_element is not None:
            marc_element.end()

    def characters(self, content):
        """
        Handles character data within an XML element.

        Args:
            content: Character data to process.
        """
        if content.strip():
            if self.current_line_count > 0:
                # Append content to the existing text for multi-line elements
                self.marc_xml_state.current_text += content
            else:
                self.current_line_count += 1
                # Set the text content for single-line elements
                self.marc_xml_state.current_text = content

class MarcXmlConversionStrategy:
    """Handles conversion between MARC XML and internal MARC records."""

    def to_records(self, src):
        """
        Parses MARC XML into a list of records.

        Args:
            src: Source of the MARC XML (file path, file-like object, or string).

        Returns:
            A list of parsed MarcRecords.
        """
        content_handler = MarcXmlHandler()
        try:
            # Parse the XML content from the provided source
            xml.sax.parse(src, content_handler)
        except FinishedParsing:
            pass
        return content_handler.marc_xml_state.records

    def from_records(self, src):
        """
        Converts a list of MARC records to MARC XML format.

        Args:
            src: List of MARC records to convert.

        Returns:
            Root element of the MARC XML.
        """
        ns = {
            "marc": "http://www.loc.gov/MARC21/slim",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }
        for prefix, uri in ns.items():
            ET.register_namespace(prefix, uri)

        root = ET.Element(
            "{http://www.loc.gov/MARC21/slim}collection",
            {
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd"
            },
        )

        for record in src:
            record_elem = ET.SubElement(root, "{http://www.loc.gov/MARC21/slim}record")

            leader_elem = ET.SubElement(record_elem, "{http://www.loc.gov/MARC21/slim}leader")
            leader_elem.text = escape(record.leader.value)

            for field in record.controlfields:
                control_field = ET.SubElement(
                    record_elem,
                    "{http://www.loc.gov/MARC21/slim}controlfield",
                    tag=field.tag,
                )
                control_field.text = escape(field.values[0])

            for field in record.data_fields:
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
