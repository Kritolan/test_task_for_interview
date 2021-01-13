from csv import DictReader
from pathlib import Path
from typing import Any, List
from xml.etree import ElementTree as ET

import ijson

from test_task.record import Record


def read_file(file_path: Path) -> List[Record]:
    handlers = {".csv": _read_csv, ".json": _read_json, ".xml": _read_xml}
    if file_path.suffix in handlers:
        return handlers[file_path.suffix](file_path)
    else:
        print(f"{file_path.suffix} files are not supported")
        return []


def _read_csv(file_path: Path) -> List[Record]:
    data = []

    with open(file_path, "r") as f:
        reader = DictReader(f, delimiter=",")
        for line in reader:
            dimensions, marks = {}, {}
            for k, v in line.items():
                if "D" in k:
                    dimensions[k] = v
                elif "M" in k:
                    marks[k] = int(v)
            data.append(Record(dimensions, marks))

    return data


def _read_json(file_path: Path) -> List[Record]:
    data = []

    with open(file_path, "rb") as f:
        objects = ijson.items(f, "fields.item")
        for obj in objects:
            dimensions, marks = {}, {}
            for k, v in obj.items():
                if "D" in k:
                    dimensions[k] = v
                elif "M" in k:
                    marks[k] = v
            data.append(Record(dimensions, marks))

    return data


def _read_xml(file_path: Path) -> List[Record]:
    data, dimensions, marks = [], {}, {}

    tree = ET.parse(file_path)
    for obj in tree.getroot()[0]:
        name: str = obj.attrib["name"]
        value: Any = obj[0].text
        if "D" in name:
            dimensions[name] = value
        elif "M" in name:
            marks[name] = int(value)
    data.append(Record(dimensions, marks))

    return data
