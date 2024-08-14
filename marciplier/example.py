from marciplier.utils import download_file, extract_archive
from marciplier.converter import convert

download_file(url="https://data.digar.ee/erb/ERB_eestikeelne_raamat.zip", filename="ERB_eestikeelne_raamat.zip", folder="data")
src = extract_archive(archive_path="data/ERB_eestikeelne_raamat.zip", extract_to="data")

result = convert(src, src_format="xml", target_format="records")
print(len(result))
