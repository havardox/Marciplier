import os
from pathlib import Path
import tarfile
from xml.dom import minidom
import zipfile

import py7zr
import requests


def prettify_xml(xml_str, indent: str = "\t"):
    """Return a pretty-printed XML string for the Element."""

    reparsed = minidom.parseString(xml_str)
    return reparsed.toprettyxml(indent=indent)


def download_file(
    url: str, folder: os.PathLike | str, filename: str | None = None, **requests_kwargs
) -> Path:
    download_path = Path(folder)
    download_path.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, **requests_kwargs)
    response.raise_for_status()
    if filename is None:
        content_dispostion = response.headers.get("content-disposition")
        if content_dispostion is None:
            raise ValueError(
                "Unable to determine filename because no Content-Dispositon header was found for the request performed on the URL. Please provide the download_filename argument."
            )
        filename = content_dispostion.split("=", -1)[-1]

    download_path = download_path / filename

    with open(download_path, "wb") as f:
        f.write(response.content)
    return download_path


def extract_archive(
    archive_path: os.PathLike | str, extract_to: os.PathLike | str
) -> Path:
    archive_path = Path(archive_path)
    extract_to = Path(extract_to)

    if archive_path.suffix == ".zip":
        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(extract_to)
            return extract_to / archive.namelist()[0]
    elif archive_path.suffix in {".tar", ".tar.gz", ".tgz"}:
        with tarfile.open(archive_path, "r:*") as archive:
            archive.extractall(extract_to)
            return extract_to / archive.getnames()[0]
    elif archive_path.suffix == ".7z":
        with py7zr.SevenZipFile(archive_path, "r") as archive:
            archive.extractall(path=extract_to)
            return extract_to / archive.getnames()[0]
    else:
        raise ValueError(f"Unsupported archive format: {archive_path.suffix}")
    

