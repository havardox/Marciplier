import os
from pathlib import Path
from typing import Union, Optional, List
import json
from xml.etree import ElementTree as ET
from marciplier.converters.json_to_records import json_to_records
from marciplier.converters.records_to_marcxml import records_to_marcxml
from marciplier.converters.marcxml_to_records import marcxml_to_records
from marciplier.converters.records_to_json import records_to_json
from marciplier.marc_record import MarcRecord
from marciplier.utils import extract_archive, download_file, prettify_xml


class MarcAdapter:
    def read(self, source: Union[os.PathLike, str]) -> List[MarcRecord]:
        raise NotImplementedError

    def to_string(self, records: List[MarcRecord]) -> str:
        raise NotImplementedError

    def to_file(self, records: List[MarcRecord], output_path: Union[os.PathLike, str]) -> None:
        raise NotImplementedError
        


class MarcXmlAdapter(MarcAdapter):
    def read(self, source: Union[os.PathLike, str]) -> List[MarcRecord]:
        source = Path(source)
        if source.suffix in {".zip", ".tar", ".tar.gz", ".7z"}:
            source = extract_archive(source, source.parent)
        with open(source, "r", encoding="utf-8") as file:
            return marcxml_to_records(records=file)

    @staticmethod
    def to_string(
        records: List[MarcRecord], prettify: bool = False, indent: str = "\t"
    ) -> str:
        marc_xml = ET.tostring(records_to_marcxml(records=records), encoding="unicode")
        marc_xml = f'<?xml version="1.0" encoding="UTF-8" ?>{marc_xml}'
        if prettify:
            marc_xml = prettify_xml(marc_xml, indent=indent)
        return marc_xml

    @staticmethod
    def to_file(
        records: List[MarcRecord],
        output_path: Union[os.PathLike, str],
        prettify: bool = False,
        indent: str = "\t",
    ) -> None:
        output_path = Path(output_path)
        marc_xml_str = MarcXmlAdapter.to_string(
            records=records, prettify=prettify, indent=indent
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(marc_xml_str)


class MarcJsonAdapter(MarcAdapter):
    def read(self, source: Union[os.PathLike, str]) -> List[MarcRecord]:
        source = Path(source)
        if source.suffix in {".zip", ".tar", ".tar.gz", ".7z"}:
            source = extract_archive(source, Path("."))
        with open(source, "r", encoding="utf-8") as file:
            marc_json = json.load(file)
            if not isinstance(marc_json, list):
                raise ValueError("Incorrect JSON format for MarcRecords")
        return json_to_records(marc_json)

    @staticmethod
    def to_string(
        records: List[MarcRecord],
        prettify: bool = False,
        indent: Optional[Union[str, int]] = None,
    ) -> str:
        return records_to_json(records=records, indent=indent if prettify else None)

    @staticmethod
    def to_file(
        records: List[MarcRecord],
        output_path: Union[os.PathLike, str],
        prettify: bool = False,
        indent: Optional[Union[str, int]] = None,
    ) -> None:
        output_path = Path(output_path)
        json_str = MarcJsonAdapter.to_string(
            records=records, prettify=prettify, indent=indent
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)


class MarcHandler:
    def __init__(self, src: str, src_format: str, download: bool = False, download_folder: Optional[str] = None, download_filename: Optional[str] = None):
        self.src = src
        self.src_format = src_format
        self.download = download
        self.download_folder = Path(download_folder) if download_folder else Path(".")
        self.download_filename = download_filename
        self.records: List[MarcRecord] = []

        if self.download:
            self.src_path = download_file(self.src, self.download_folder, self.download_filename)
        else:
            self.src_path = Path(self.src)
        self._read_records()


    def _read_records(self) -> None:
        adapter = self._get_adapter()
        self.records = adapter.read(self.src_path)

    def _get_adapter(self) -> MarcAdapter:
        if self.src_format == "xml":
            return MarcXmlAdapter()
        elif self.src_format == "json":
            return MarcJsonAdapter()
        else:
            raise ValueError("Unsupported format")

    def to_xml(self, output_path: Union[os.PathLike, str], prettify: bool = False, indent: str = "\t") -> None:
        adapter = MarcXmlAdapter()
        adapter.to_file(self.records, output_path, prettify, indent)

    def to_json(self, output_path: Union[os.PathLike, str], prettify: bool = False, indent: Optional[Union[str, int]] = None) -> None:
        adapter = MarcJsonAdapter()
        adapter.to_file(self.records, output_path, prettify, indent)