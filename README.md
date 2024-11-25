# Marciplier

I wrote this because I couldn't find a good tool that converts MARCXML to JSON at an okay-ish speed. This program is memory efficient and fast as it uses Python's Simple API for XML (SAX) to parse the XML. SAX is a streaming API and doesn't load the entire XML tree into memory. This program works pretty well with large files (2 GB and upwards).

The JSON format is by own intuition. I don't think there's any recognized standard for a JSON representation of MARC 21.

If you found this repo through Google, please do consider giving it a star. It really does help.

## Installation

1\. Install [Python](https://wiki.python.org/moin/BeginnersGuide/Download)

(From your project directory)

2\. python -m venv venv

3\. Unix/MacOS: source venv/bin/activate

&emsp;Windows: venv\Scripts\activate

4\. pip install git+https://github.com/havardox/Marciplier.git

## How to Use

Here's a simple example of how to use Marciplier to convert a MARCXML file to JSON format:

```python
import json

from marciplier.converter import convert
from marciplier.utils import download_file, extract_archive


download_file(url="https://data.digar.ee/erb/ERB_perioodika.zip", filename="ERB_perioodika.zip", folder="data")
src = extract_archive(archive_path="data/ERB_perioodika.zip", extract_to="data")[0]

xml_to_json_result = convert(src, src_format="xml", target_format="json")

print(f"File contains {len(xml_to_json_result)} records.")

# Save to JSON
with open ("data/ERB_perioodika1.json", "w") as f:
    json.dump(obj=xml_to_json_result, fp=f)
```

`File contains 18692 records.`


## Benchmark

```python
import timeit

from marciplier.converter import convert
from marciplier.utils import download_file, extract_archive


download_file(url="https://data.digar.ee/erb/ERB_eestikeelne_raamat.zip", filename="ERB_eestikeelne_raamat.zip", folder="data")
src = extract_archive(archive_path="data/ERB_eestikeelne_raamat.zip", extract_to="data")[0]

start = timeit.default_timer()
result = convert(src, src_format="xml", target_format="records")
end = timeit.default_timer()

print(f"Benchmark took {end - start:.2f} seconds or {len(result) / (end - start):.2f} records per second.")
```

`Benchmark took 106.86 seconds or 2090.41 records per second.`
