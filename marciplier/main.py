import json
from pathlib import Path
from marciplier.analyze_marc_records import analyze_marc_records
from marciplier.marc_handler import MarcHandler

marc_handler_1 = MarcHandler(
    src="https://data.digar.ee/erb/ERB_eestikeelne_raamat.zip",
    download=True,
    download_folder="data",
    download_filename="ERB_eestikeelne_raamat.zip",
    src_format="xml",
)
marc_handler_1.to_json(Path("data") / "data1.json")
marc_handler_1.to_xml(Path("data") / "data1.xml")

marc_handler_2 = MarcHandler(src="data/data1.json", src_format="json")

marc_handler_2.to_json(Path("data") / "data2.json")
marc_handler_2.to_xml(Path("data") / "data2.xml")
