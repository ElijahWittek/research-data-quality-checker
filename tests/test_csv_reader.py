import pytest

from research_data_quality_checker.csv_reader import read_csv_file


def test_read_csv_file_returns_columns_and_rows(tmp_path):
    file_path = tmp_path / "valid.csv"

    file_path.write_text(
        "measurement_id,station_id,measurement_date,"
        "temperature_c,humidity_percent,pressure_hpa\n"
        "1001,BERLIN_01,2026-08-10,24.7,58.0,1012.4\n"
        "1002,POTSDAM_01,2026-08-11,25.2,55.3,1011.6\n",
        encoding="utf-8",
    )

    columns, rows = read_csv_file(str(file_path))

    assert columns == [
        "measurement_id",
        "station_id",
        "measurement_date",
        "temperature_c",
        "humidity_percent",
        "pressure_hpa",
    ]
    assert len(rows) == 2
    assert rows[0]["measurement_id"] == "1001"
    assert rows[1]["station_id"] == "POTSDAM_01"

def test_read_csv_file_raises_error_for_missing_file(tmp_path):
    file_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        read_csv_file(str(file_path))