from marciplier.utils import download_file, extract_archive
from marciplier.converter import convert
import timeit


download_file(url="https://data.digar.ee/erb/ERB_eestikeelne_raamat.zip", filename="ERB_eestikeelne_raamat.zip", folder="data")
src = extract_archive(archive_path="data/ERB_eestikeelne_raamat.zip", extract_to="data")[0]

start = timeit.default_timer()
result = convert(src, src_format="xml", target_format="records")
end = timeit.default_timer()

print(f"Benchmark took {end - start:.2f} seconds or {len(result) / (end - start):.2f} records per second.")
