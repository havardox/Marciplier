# Marciplier

I wrote this because I couldn't find a good tool that converts MARCXML to JSON at an okay-ish speed. This program is memory efficient and fast as it uses Python's Simple API for XML (SAX) to parse the XML. SAX is a streaming API and doesn't load the entire XML tree into memory. This program works pretty well with large files (2 GB and upwards).

The JSON format is by own intuition. I don't think there's any recognized standard for a JSON representation of MARC 21.

If you found this repo through Google, please do consider giving it a star. It really does help.

## Installation

1\. Install [Python](https://wiki.python.org/moin/BeginnersGuide/Download)

(Run the below commands from your project directory)

2\. `python -m venv venv`

3\. Unix/MacOS: `source venv/bin/activate`

&emsp;Windows: `venv\Scripts\activate`

4\. `pip install git+https://github.com/havardox/Marciplier.git`

## How to Use

Here's a simple example of how to use Marciplier to convert a MARCXML file to JSON format:

```python
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

pprint(xml_to_json_result[0])

# Save to JSON
with open("data/ERB_perioodika.json", "w") as f:
    json.dump(obj=xml_to_json_result, fp=f)
```

```
File contains 18692 records.

{'controlfields': {'001': ['b10009784'],
                   '003': ['ErRR'],
                   '008': ['981126d19621962er ar  | ||||||   |0rus  ']},
 'datafields': {'040': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['ErTTUR']},
                                       {'b': ['est']},
                                       {'c': ['ErTTUR']},
                                       {'d': ['ErRR']}]}],
                '042': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['nbr']}]}],
                '072': [{'indicators': (' ', '7'),
                         'subfields': [{'a': ['621.3']}, {'2': ['udkrb']}]}],
                '080': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['621.3']},
                                       {'x': ['(06)']},
                                       {'2': ['est']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'a': ['378.662']},
                                       {'x': ['(474.2)', '(06)']},
                                       {'2': ['est']}]}],
                '130': [{'indicators': ('0', ' '),
                         'subfields': [{'a': ['Tallinna Polütehnilise '
                                              'Instituudi toimetised.']},
                                       {'p': ['Труды по электротехнике']}]}],
                '245': [{'indicators': ('1', '0'),
                         'subfields': [{'a': ['Tallinna Polütehnilise '
                                              'Instituudi toimetised.']},
                                       {'n': ['Seeria A,']},
                                       {'p': ['Труды по электротехнике =']},
                                       {'b': ['Труды Таллинского '
                                              'политехнического института. '
                                              'Серия A. Труды по '
                                              'электротехнике : сборник '
                                              'статей']}]}],
                '246': [{'indicators': ('1', '1'),
                         'subfields': [{'a': ['Труды Таллинского '
                                              'политехнического института.']},
                                       {'n': ['Серия А,']},
                                       {'p': ['Труды по электротехнике']}]},
                        {'indicators': ('1', '3'),
                         'subfields': [{'a': ['Труды по электротехнике']}]}],
                '260': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['Таллин :']},
                                       {'b': ['Таллинский политехнический '
                                              'институт,']},
                                       {'c': ['1962.']}]}],
                '300': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['1 kd. ;']}, {'c': ['20 cm.']}]}],
                '310': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['Üks kord aastas.']}]}],
                '504': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['Sisaldab bibliograafiat.']}]}],
                '580': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['Jätkab pealkirjaga: Tallinna '
                                              'Polütehnilise Instituudi '
                                              'toimetised. Seeria A, Труды по '
                                              'электротехнике и автоматике '
                                              '(1963-1971)']}]}],
                '650': [{'indicators': (' ', '4'),
                         'subfields': [{'a': ['elektrotehnika']},
                                       {'0': ['https://ems.elnet.ee/id/EMS002078.']}]},
                        {'indicators': (' ', '4'),
                         'subfields': [{'a': ['tehnikakõrgkoolid']},
                                       {'0': ['https://ems.elnet.ee/id/EMS006962.']}]}],
                '651': [{'indicators': (' ', '4'),
                         'subfields': [{'a': ['Eesti (riik)']},
                                       {'0': ['https://ems.elnet.ee/id/EMS131705.']}]}],
                '655': [{'indicators': (' ', '4'),
                         'subfields': [{'a': ['toimetised.']}]}],
                '710': [{'indicators': ('2', ' '),
                         'subfields': [{'a': ['Tallinna Polütehniline '
                                              'Instituut.']}]}],
                '760': [{'indicators': ('0', ' '),
                         'subfields': [{'t': ['Tallinna Polütehnilise '
                                              'Instituudi toimetised']},
                                       {'g': ['1947-1989.']},
                                       {'x': ['0136-3549']},
                                       {'w': ['b12903887.']}]}],
                '785': [{'indicators': ('1', '0'),
                         'subfields': [{'t': ['Tallinna Polütehnilise '
                                              'Instituudi toimetised. '
                                              'Электротехника и автоматика.']},
                                       {'g': ['1963-1988.']},
                                       {'x': ['0134-3823']},
                                       {'w': ['b14205269.']}]}],
                '866': [{'indicators': (' ', '0'),
                         'subfields': [{'a': ['RR: 1962.']}]},
                        {'indicators': (' ', '0'),
                         'subfields': [{'a': ['TLUAR: 1962.']}]}],
                '907': [{'indicators': (' ', ' '),
                         'subfields': [{'a': ['.b10009784']},
                                       {'b': ['multi']},
                                       {'c': ['r']}]}],
                '910': [{'indicators': ('0', ' '),
                         'subfields': [{'a': ['PER 1945-1998']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'a': ['ERB 1962']}]}],
                '945': [{'indicators': (' ', ' '),
                         'subfields': [{'l': ['apk  ']},
                                       {'a': ['Ep.6.7/193']},
                                       {'u': ['193 [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['apk  ']},
                                       {'a': ['Ep.6.7/193']},
                                       {'u': ['193 [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['apk  ']},
                                       {'a': ['Ep.6.7/193']},
                                       {'u': ['193 [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['rarkh']},
                                       {'a': ['AR J-52']},
                                       {'u': ['193 [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['r4eks']},
                                       {'a': ['PE A/7; 193 [1]']},
                                       {'u': ['193 [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['r4jtk']},
                                       {'a': ['PE A/7; 193 [2]']},
                                       {'u': ['193 [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['r4jtk']},
                                       {'a': ['PE A/7; 193 [3]']},
                                       {'u': ['193 [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['r4jtk']},
                                       {'a': ['PE A/7; 193 [4]']},
                                       {'u': ['193 [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['ttho2']},
                                       {'a': ['A-86886']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['ttho2']},
                                       {'a': ['A-86887']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['ttho2']},
                                       {'a': ['A-86888']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['ttho2']},
                                       {'a': ['A-86889']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['tt2st']},
                                       {'a': ['378TTÜ/T-193']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['ttho2']},
                                       {'a': ['A-86891']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['ttho2']},
                                       {'a': ['A-86892']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['tt4tt']},
                                       {'a': ['621.3/T-193']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['tbiar']},
                                       {'a': ['TTUarh-2']},
                                       {'u': ['1 (193) [1962]']}]},
                        {'indicators': (' ', ' '),
                         'subfields': [{'l': ['yyark']},
                                       {'a': ['ARH Per.A-1459']},
                                       {'u': ['193 [1962]']}]}]},
 'leader': '03145nas a22006611i 4500'}
```

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
