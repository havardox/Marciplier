import json
from pprint import pprint

from marciplier.converter import convert
from marciplier.utils import download_file, extract_archive


download_file(
    url="https://data.digar.ee/erb/ERB_perioodika.zip",
    filename="ERB_perioodika.zip",
    folder="data",
)
src = extract_archive(archive_path="data/ERB_perioodika.zip", extract_to="data")[0]

xml_to_json_result = convert(src, src_format="xml", target_format="json")

print(f"File contains {len(xml_to_json_result)} records.\n")

print("First record:\n")

pprint(xml_to_json_result[0])

print("\nSaving to JSON file...")

with open("data/ERB_perioodika.json", "w") as f:
    json.dump(obj=xml_to_json_result, fp=f)
