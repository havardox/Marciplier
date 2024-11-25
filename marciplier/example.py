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
