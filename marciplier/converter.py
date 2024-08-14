from typing import Any, Literal, Union
from marciplier.converters.marc_json import MarcJsonConversionStrategy
from marciplier.converters.marc_xml import MarcXmlConversionStrategy
from marciplier.conversion_strategy import ConversionStrategy


STRATEGIES: dict[str, ConversionStrategy | Literal["records"]] = {
    "json": MarcJsonConversionStrategy(),
    "xml": MarcXmlConversionStrategy(),
    "records": "records"
}

def convert(src: Any, src_format: str, target_format: str) -> Union[dict, list, str]:
    if src_format not in STRATEGIES or target_format not in STRATEGIES:
        raise ValueError(f"Unsupported format: {src_format} or {target_format}")

    src_strategy = STRATEGIES[src_format]
    target_strategy = STRATEGIES[target_format]

    result = src
    if src_format != "records":
        result = src_strategy.to_records(src)
    if target_format != "records":
        return target_strategy.from_records(result)
    return result