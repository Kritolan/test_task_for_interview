from pathlib import Path
from typing import List

from test_task.handlers import read_file
from test_task.record import AdvancedListRecords, BasicListRecords, Record


def collect_data(data_dir: Path) -> List[Record]:
    data: List[Record] = []
    for file in data_dir.iterdir():
        data.extend(read_file(file))

    return data


def main() -> None:
    data_dir: Path = Path.cwd() / "data"
    data: List[Record] = collect_data(data_dir)

    basic_data = BasicListRecords(data)
    basic_path = Path.cwd() / "results" / "basic_results.tsv"
    basic_data.save(basic_path)

    advanced_data = AdvancedListRecords(data)
    advanced_path = Path.cwd() / "results" / "advanced_results.tsv"
    advanced_data.save(advanced_path)


if __name__ == "__main__":
    main()
