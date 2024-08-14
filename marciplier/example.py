from marciplier.utils import download_file, extract_archive
from marciplier.converter import convert

download_file(url="https://data.digar.ee/erb/ERB_perioodika.zip", filename="ERB_perioodika.zip", folder="data")
src = extract_archive(archive_path="data/ERB_perioodika.zip", extract_to="data")

result = convert(src, src_format="xml", target_format="json")
print(f"File contains {len(result)} records.")
