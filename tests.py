from pathlib import Path
from typing import Callable, List

from pytest import fixture

from test_task.main import collect_data
from test_task.record import AdvancedListRecords, BasicListRecords, Record


@fixture(scope="module")
def create_files():  # type: ignore
    data_dir: Path = Path.cwd() / "data"
    data: List[Record] = collect_data(data_dir)

    basic_data = BasicListRecords(data)
    basic_path = Path.cwd() / "results" / "test_basic_results.tsv"
    basic_data.save(basic_path)

    advanced_data = AdvancedListRecords(data)
    advanced_path = Path.cwd() / "results" / "test_advanced_results.tsv"
    advanced_data.save(advanced_path)

    yield

    basic_path.unlink()
    advanced_path.unlink()


def test_basic(create_files: Callable[[None], None]) -> None:
    res_path = Path.cwd() / "results" / "test_basic_results.tsv"
    ref_path = Path.cwd() / "references" / "basic_results.tsv"
    with open(res_path) as res_file, open(ref_path) as ref_file:
        assert list(res_file) == list(ref_file)


def test_advanced(create_files: Callable[[None], None]) -> None:
    res_path = Path.cwd() / "results" / "test_advanced_results.tsv"
    ref_path = Path.cwd() / "references" / "advanced_results.tsv"
    with open(res_path) as res_file, open(ref_path) as ref_file:
        assert list(res_file) == list(ref_file)
