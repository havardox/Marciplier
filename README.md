# Marciplier

I wrote this because I couldn't find a good tool that converts MARCXML to JSON at an okay-ish speed. This program is memory efficient and fast as it uses Python's Simple API for XML (SAX) to parse the XML. SAX is a streaming API and doesn't load the entire XML tree into memory. This program works pretty well with large files (2 GB and upwards).

The JSON format is by own intuition. I don't think there's any recognized standard for a JSON representation of MARC 21.

If you found this repo through Google, please do consider giving it a star. It really does help.

## Installation

```python
(From your project directory)
1. python -m venv venv

Windows:
2. venv\Scripts\activate

Unix/MacOS:
2. source venv/bin/activate

3. pip install git+https://github.com/havardox/Marciplier.git
```

## How to Use

Here's a simple example of how to use Marciplier to convert a MARCXML file to JSON format:

```python
import json

from marciplier.converter import convert
from marciplier.marc_record import MarcRecord
from marciplier.utils import download_file, extract_archive


download_file(url="https://data.digar.ee/erb/ERB_perioodika.zip", filename="ERB_perioodika.zip", folder="data")
src = extract_archive(archive_path="data/ERB_perioodika.zip", extract_to="data")[0]

xml_to_json_result = convert(src, src_format="xml", target_format="json")

with open ("data/ERB_perioodika1.json", "w") as f:
    json.dump(obj=xml_to_json_result, fp=f)

xml_to_records_result: list[MarcRecord] = convert(src, src_format="xml", target_format="records")
for record in xml_to_records_result[:10]:
    print(record.get_data_field("245")[0].get_subfield("a").values[0])
```
```
File contains 18692 records.
```

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
