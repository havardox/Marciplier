import os
from pathlib import Path
import tarfile
from xml.dom import minidom
import zipfile

import py7zr
import requests


def prettify_xml(xml_str: str, indent: str = "\t") -> str:
    """
    Returns a pretty-printed XML string.

    Args:
        xml_str: A string containing the XML to be formatted.
        indent: A string to use for indentation. Defaults to a tab character.

    Returns:
        The formatted XML string.
    """
    reparsed = minidom.parseString(xml_str)
    return reparsed.toprettyxml(indent=indent)


def download_file(
    url: str, folder: os.PathLike | str, filename: str | None = None, **requests_kwargs
) -> Path:
    """
    Downloads a file from the given URL and saves it to the specified folder.

    Args:
        url: The URL of the file to download.
        folder: The directory where the downloaded file should be saved.
        filename: Optional; the name to save the file as. If not provided, attempts to derive the
                  filename from the `Content-Disposition` header.
        **requests_kwargs: Additional keyword arguments to pass to the `requests.get` method.

    Returns:
        The path to the downloaded file.

    Raises:
        ValueError: If the filename cannot be inferred from the response headers and is not provided.
        requests.exceptions.RequestException: For HTTP errors.
    """
    download_path = Path(folder)
    download_path.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, **requests_kwargs)
    response.raise_for_status()

    if filename is None:
        content_disposition = response.headers.get("content-disposition")
        if content_disposition is None:
            raise ValueError(
                "Unable to determine filename because no Content-Disposition header was found. "
                "Please provide the filename argument."
            )
        filename = content_disposition.split("=", -1)[-1]

    download_path = download_path / filename

    with open(download_path, "wb") as f:
        f.write(response.content)
    return download_path


def extract_archive(
    archive_path: os.PathLike | str,
    extract_to: os.PathLike | str,
    targets_to_extract: list[str] = [],
) -> list[Path]:
    """
    Extracts an archive file (zip, tar, or 7z) to a specified directory.

    Args:
        archive_path: The path to the archive file.
        extract_to: The directory where the contents of the archive should be extracted.
        targets_to_extract: Optional; a list of specific file names to extract. If empty,
                            extracts all files. Defaults to an empty list.

    Returns:
        A list of paths to the extracted files.

    Raises:
        ValueError: If the archive format is unsupported.
    """
    archive_path = Path(archive_path)
    extract_to = Path(extract_to)

    if archive_path.suffix == ".zip":
        with zipfile.ZipFile(archive_path, "r") as archive:
            if targets_to_extract:
                for target in targets_to_extract:
                    archive.extract(target, extract_to)
                return [extract_to / target for target in targets_to_extract]
            else:
                archive.extractall(extract_to)
                return [extract_to / name for name in archive.namelist()]

    elif archive_path.suffix in {".tar", ".tar.gz", ".tgz"}:
        with tarfile.open(archive_path, "r:*") as archive:
            if targets_to_extract:
                for target in targets_to_extract:
                    archive.extract(target, extract_to)
                return [extract_to / target for target in targets_to_extract]
            else:
                archive.extractall(extract_to)
                return [extract_to / name for name in archive.getnames()]

    elif archive_path.suffix == ".7z":
        with py7zr.SevenZipFile(archive_path, "r") as archive:
            if targets_to_extract:
                archive.extract(extract_to, targets_to_extract)
                return [extract_to / target for target in targets_to_extract]
            else:
                archive.extractall(extract_to)
                return [extract_to / name for name in archive.getnames()]

    else:
        raise ValueError(f"Unsupported archive format: {archive_path.suffix}")
