from research_data_quality_checker.validation import (
    get_missing_required_columns,
    get_missing_required_values,
    is_missing_value,
)


def test_all_required_columns_are_present():
    columns = [
        "measurement_id",
        "station_id",
        "measurement_date",
        "temperature_c",
        "humidity_percent",
        "pressure_hpa",
    ]

    result = get_missing_required_columns(columns)

    assert result == []

def test_missing_required_column_is_detected():
    columns = [
        "measurement_id",
        "station_id",
        "measurement_date",
        "temperature_c",
        "humidity_percent",
    ]

    result = get_missing_required_columns(columns)

    assert result == ["pressure_hpa"]

def test_additional_columns_are_allowed():
    columns = [
        "measurement_id",
        "station_id",
        "measurement_date",
        "temperature_c",
        "humidity_percent",
        "pressure_hpa",
        "wind_speed",
    ]

    result = get_missing_required_columns(columns)

    assert result == []

def test_empty_value_is_missing():
    result = is_missing_value("")

    assert result is True

def test_whitespace_only_value_is_missing():
    result = is_missing_value("  ")

    assert result is True

def test_non_empty_value_is_not_missing():
    result = is_missing_value("BERLIN_01")

    assert result is False

def test_missing_required_value_is_detected():
    row = {
        "measurement_id": "1001",
        "station_id": "",
        "measurement_date": "2026-08-10",
        "temperature_c": "24.7",
        "humidity_percent": "58.0",
        "pressure_hpa": "1012.4",
    }

    result = get_missing_required_values(row)

    assert result == ["station_id"]

def test_multiple_missing_required_values_are_detected():
    row = {
        "measurement_id": "1001",
        "station_id": "",
        "measurement_date": "2026-08-10",
        "temperature_c": "   ",
        "humidity_percent": "58.0",
        "pressure_hpa": "",
    }

    result = get_missing_required_values(row)

    assert result == [
        "station_id",
        "temperature_c",
        "pressure_hpa"
    ]

def test_missing_column_is_not_reported_as_missing_value():
    row = {
        "measurement_id": "1001",
        "station_id": "BERLIN_01",
        "measurement_date": "2026-08-10",
        "temperature_c": "24.7",
        "humidity_percent": "58.0",
    }

    result = get_missing_required_values(row)

    assert result == []