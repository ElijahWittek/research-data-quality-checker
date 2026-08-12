from research_data_quality_checker.csv_reader import read_csv_file
from research_data_quality_checker.validation import validate_dataset


def test_valid_csv_file_has_no_findings():
    columns, rows = read_csv_file("data/valid_measurements.csv")

    findings = validate_dataset(columns, rows)

    assert len(rows) == 3
    assert findings == []

def test_invalid_csv_file_collects_multiple_findings():
    columns, rows = read_csv_file("data/invalid_measurements.csv")

    findings = validate_dataset(columns, rows)

    finding_types = [finding["type"] for finding in findings]

    assert len(rows) == 3
    assert "missing_value" in finding_types
    assert "invalid_date" in finding_types
    assert "out_of_range" in finding_types
    assert "duplicate_measurement_id" in finding_types