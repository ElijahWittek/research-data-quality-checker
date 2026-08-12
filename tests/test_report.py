from research_data_quality_checker.report import (
    build_terminal_summary,
    build_text_report,
    write_text_report,
)


def test_terminal_summary_contains_required_information():
    findings = [
        {
            "type": "out_of_range",
            "row_number": 2,
            "measurement_id": "1001",
            "column": "temperature_c",
            "value": "61.2",
            "description": "Value must be between -50.0 and 60.0, inclusive.",
        }
    ]

    result = build_terminal_summary(
        "invalid_measurements.csv",
        3,
        findings,
        "validation_report.txt",
    )

    assert "File: invalid_measurements.csv" in result
    assert "Records checked: 3" in result
    assert "Issues found: 1" in result
    assert "Status: Issues found" in result
    assert "Report: validation_report.txt" in result

def test_text_report_contains_finding_details():
    findings = [
        {
            "type": "missing_value",
            "row_number": 3,
            "measurement_id": "1002",
            "column": "station_id",
            "value": "",
            "description": "Required value is missing.",
        }
    ]

    result = build_text_report(
        "invalid_measurements.csv",
        3,
        findings,
    )

    assert "File: invalid_measurements.csv" in result
    assert "Issues found: 1" in result
    assert "Type: missing_value" in result
    assert "Row: 3" in result
    assert "Measurement ID: 1002" in result
    assert "Column: station_id" in result
    assert "Value: <empty>" in result
    assert "Description: Required value is missing." in result

def test_valid_dataset_report_is_written(tmp_path):
    report_text = build_text_report(
        "valid_measurements.csv",
        3,
        [],
    )

    report_path = tmp_path / "validation_report.txt"

    write_text_report(str(report_path), report_text)

    saved_text = report_path.read_text(encoding="utf-8")

    assert "Issues found: 0" in saved_text
    assert "Status: No issues found" in saved_text
    assert "No data quality issues found." in saved_text