# Marciplier

I wrote this because I couldn't find a good tool that converts MARCXML to JSON at an okay-ish speed. This program is memory efficient and fast as it uses Python's Simple API for XML (SAX) to parse the XML. SAX is a streaming API and doesn't load the entire XML tree into memory. This program works pretty well with large files (2 GB and upwards).

The JSON format is by own intuition. I don't think there's a any recognized standard for a JSON representation of MARC 21.

If you found this repo through Google, please do consider giving it a star. It really does help.

## Installation

```python
(From your project directory)
1. python -m venv venv

Windows:
2. venv\Scripts\activate

Unix/MacOS:
2. source venv/bin/activate

3. pip install https://github.com/havardox/Marciplier.git
```

## How to Use

Here's a simple example of how to use Marciplier to convert a MARCXML file to JSON format:

```python
from marciplier.utils import download_file, extract_archive
from marciplier.converter import convert

download_file(url="https://data.digar.ee/erb/ERB_perioodika.zip", filename="ERB_perioodika.zip", folder="data")
src = extract_archive(archive_path="data/ERB_perioodika.zip", extract_to="data")

result = convert(src, src_format="xml", target_format="json")
print(f"File contains {len(result)} records.")
```

`File contains 18608 records.`


## Benchmark

```python
from marciplier.utils import download_file, extract_archive
from marciplier.converter import convert
import timeit


download_file(url="https://data.digar.ee/erb/ERB_eestikeelne_raamat.zip", filename="ERB_eestikeelne_raamat.zip", folder="data")
src = extract_archive(archive_path="data/ERB_eestikeelne_raamat.zip", extract_to="data")

start = timeit.default_timer()
result = convert(src, src_format="xml", target_format="records")
end = timeit.default_timer()

print(f"Benchmark took {end - start:.2f} seconds or {len(result) / (end - start):.2f} records per second.")
```

`Benchmark took 96.44 seconds or 2299.96 records per second.`