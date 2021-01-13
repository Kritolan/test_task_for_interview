from csv import DictWriter
from pathlib import Path
from typing import Any, Dict, List, Union


class Record:
    def __init__(self, dimensions: Dict[str, str], marks: Dict[str, int]):
        self.dimensions: Dict[str, str] = dimensions
        self.marks: Dict[str, int] = marks
        self.key: str = "".join([self.dimensions[d] for d in sorted(dimensions)])


class _ListRecords:
    def __init__(self, list_records: List[Record]):
        self.records: List[Dict[str, Any]] = []
        self.fieldnames: List[str] = []

        self._create_records(list_records)

    def _create_records(self, list_records: List[Record]) -> None:
        pass

    def save(self, file_path: Path) -> None:
        with open(file_path, "w") as f:
            writer = DictWriter(f, self.fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(self.records)


class BasicListRecords(_ListRecords):
    def _create_records(self, list_records: List[Record]) -> None:
        dimensions_number: int = min(
            map(lambda record: len(record.dimensions), list_records)
        )
        marks_number: int = min(map(lambda record: len(record.marks), list_records))

        dimensions_headers: List[str] = [
            f"D{num}" for num in range(1, dimensions_number + 1)
        ]
        marks_headers: List[str] = [f"M{num}" for num in range(1, marks_number + 1)]
        self.fieldnames.extend(dimensions_headers + marks_headers)

        for record in sorted(list_records, key=lambda record: record.key):
            new_record: Dict[str, Union[str, int]] = {}
            for header in dimensions_headers:
                new_record[header] = record.dimensions[header]
            for header in marks_headers:
                new_record[header] = record.marks[header]
            self.records.append(new_record)


class AdvancedListRecords(_ListRecords):
    def _create_records(self, list_records: List[Record]) -> None:
        dimensions_number: int = min(
            map(lambda record: len(record.dimensions), list_records)
        )
        marks_number: int = min(map(lambda record: len(record.marks), list_records))

        dimensions_headers: List[str] = [
            f"D{num}" for num in range(1, dimensions_number + 1)
        ]
        marks_headers: List[str] = [f"MS{num}" for num in range(1, marks_number + 1)]
        self.fieldnames.extend(dimensions_headers + marks_headers)

        new_records: Dict[str, Dict[str, Any]] = {}
        for record in sorted(list_records, key=lambda record: record.key):
            if record.key in new_records:
                for i, header in enumerate(marks_headers):
                    new_records[record.key][header] += record.marks[f"M{i+1}"]
            else:
                new_records[record.key] = {}
                for header in dimensions_headers:
                    new_records[record.key][header] = record.dimensions[header]
                for i, header in enumerate(marks_headers):
                    new_records[record.key][header] = record.marks[f"M{i+1}"]
        self.records = list(new_records.values())
