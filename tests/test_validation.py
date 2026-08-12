from research_data_quality_checker.validation import (
    get_duplicate_measurement_ids,
    get_missing_required_columns,
    get_missing_required_values,
    get_out_of_range_values,
    is_decimal_number,
    is_missing_value,
    is_positive_integer,
    is_valid_date,
    is_within_range,
    validate_dataset,
    validate_row,
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

def test_positive_integer_is_valid():
    result = is_positive_integer("1001")

    assert result is True

def test_non_numeric_measurement_id_is_invalid():
    result = is_positive_integer("abc")

    assert result is False

def test_zero_measurement_is_invalid():
    result = is_positive_integer("0")

    assert result is False

def test_negative_measurement_id_is_invalid():
    result = is_positive_integer("-5")

    assert result is False

def test_decimal_number_is_valid():
    result = is_decimal_number("24.7")

    assert result is True

def test_non_nummeric_decimal_value_is_invalid():
    result = is_decimal_number("warm")

    assert result is False

def test_negative_decimal_number_is_valid():
    result = is_decimal_number("-12.5")

    assert result is True

def test_valid_date_is_accepted():
    result = is_valid_date("2026-08-10")

    assert result is True

def test_invalid_calender_date_is_rejected():
    result = is_valid_date("2026-02-30")

    assert result is False

def test_date_with_wrong_format_is_rejected():
    result = is_valid_date("2026-8-10")

    assert result is False

def test_duplicate_measurement_ids_is_detected():
    measurement_ids = ["1001", "1002", "1001"]

    result = get_duplicate_measurement_ids(measurement_ids)

    assert result == ["1001"]

def test_unique_measurement_ids_are_not_duplicates():
    measurement_ids = ["1001", "1002", "1003"]

    result = get_duplicate_measurement_ids(measurement_ids)

    assert result == []

def test_repeated_measurement_ids_is_reported_once():
    measurement_ids = ["1001", "1001", "1001"]

    result = get_duplicate_measurement_ids(measurement_ids)

    assert result == ["1001"]

def test_value_within_range_is_valid():
    result = is_within_range("24.7", -50.0, 60.0)

    assert result is True

def test_value_on_lower_range_boundary_is_valid():
    result = is_within_range("-50.0", -50.0, 60.0)

    assert result is True

def test_value_on_upper_range_boundary_is_valid():
    result = is_within_range("60.0", -50.0, 60.0)

    assert result is True

def test_value_above_upper_range_boundary_is_invalid():
    result = is_within_range("60.1", -50.0, 60.0)

    assert result is False

def test_value_below_lower_range_boundary_is_invalid():
    result = is_within_range("-50.1", -50.0, 60.0)

    assert result is False

def test_out_of_range_temperature_is_detected():
    row = {
        "measurement_id": "1001",
        "station_id": "BERLIN_01",
        "measurement_date": "2026-08-10",
        "temperature_c": "61.2",
        "humidity_percent": "58.0",
        "pressure_hpa": "1012.4",
    }

    result = get_out_of_range_values(row)

    assert result == ["temperature_c"]

def test_multiple_out_of_range_values_are_detected():
    row = {
        "measurement_id": "1001",
        "station_id": "BERLIN_01",
        "measurement_date": "2026-08-11",
        "temperature_c": "61.2",
        "humidity_percent": "105.0",
        "pressure_hpa": "840.0",
    }

    result = get_out_of_range_values(row)

    assert result == [
        "temperature_c",
        "humidity_percent",
        "pressure_hpa"
    ]

def test_values_on_measurement_boundaries_are_valid():
    row = {
        "measurement_id": "1001",
        "station_id": "BERLIN_01",
        "measurement_date": "2026-08-11",
        "temperature_c": "-50.0",
        "humidity_percent": "100.0",
        "pressure_hpa": "1100.0",
    }

    result = get_out_of_range_values(row)

    assert result == []

def test_non_numeric_value_is_not_reported_as_out_of_range():
    row = {
        "measurement_id": "1001",
        "station_id": "BERLIN_01",
        "measurement_date": "2026-08-11",
        "temperature_c": "warm",
        "humidity_percent": "58.0",
        "pressure_hpa": "1012.4",
    }

    result = get_out_of_range_values(row)

    assert result == []

def test_valid_row_has_no_findings():
    row = {
        "measurement_id": "1001",
        "station_id": "BERLIN_01",
        "measurement_date": "2026-08-11",
        "temperature_c": "24.7",
        "humidity_percent": "58.0",
        "pressure_hpa": "1012.4",
    }

    result = validate_row(row, 2)

    assert result == []

def test_validate_row_collects_multiple_findings():
    row = {
        "measurement_id": "1001",
        "station_id": "",
        "measurement_date": "2026-02-30",
        "temperature_c": "61.2",
        "humidity_percent": "58.0",
        "pressure_hpa": "1012.4",
    }

    result = validate_row(row, 2)

    assert len(result) == 3

    assert result[0]["type"] == "missing_value"
    assert result[0]["column"] == "station_id"

    assert result[1]["type"] == "invalid_date"
    assert result[1]["column"] == "measurement_date"

    assert result[2]["type"] == "out_of_range"
    assert result[2]["column"] == "temperature_c"

def test_valid_dataset_has_no_findings():
    columns = [
        "measurement_id",
        "station_id",
        "measurement_date",
        "temperature_c",
        "humidity_percent",
        "pressure_hpa",
    ]

    rows = [
        {
            "measurement_id": "1001",
            "station_id": "BERLIN_01",
            "measurement_date": "2026-08-10",
            "temperature_c": "24.7",
            "humidity_percent": "58.0",
            "pressure_hpa": "1012.4",
        },
        {
            "measurement_id": "1002",
            "station_id": "POTSDAM_01",
            "measurement_date": "2026-08-11",
            "temperature_c": "25.2",
            "humidity_percent": "55.3",
            "pressure_hpa": "1011.6",
        },
    ]

    result = validate_dataset(columns, rows)

    assert result == []

def test_dataset_collects_structural_row_and_duplicate_findings():
    columns = [
        "measurement_id",
        "station_id",
        "measurement_date",
        "temperature_c",
        "humidity_percent",
    ]

    rows = [
        {
            "measurement_id": "1001",
            "station_id": "BERLIN_01",
            "measurement_date": "2026-08-10",
            "temperature_c": "24.7",
            "humidity_percent": "58.0",
        },
        {
            "measurement_id": "1001",
            "station_id": "",
            "measurement_date": "2026-02-30",
            "temperature_c": "61.2",
            "humidity_percent": "55.0",
        },
    ]

    result = validate_dataset(columns, rows)

    finding_types = [finding["type"] for finding in result]

    assert "missing_column" in finding_types
    assert "duplicate_measurement_id" in finding_types
    assert "missing_value" in finding_types
    assert "invalid_date" in finding_types
    assert "out_of_range" in finding_types