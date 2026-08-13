from research_data_quality_checker.main import main


def test_main_processes_invalid_csv_and_writes_report(tmp_path, capsys):
    report_path = tmp_path / "validation_report.txt"

    exit_code = main(
        "data/invalid_measurements.csv",
        str(report_path),
    )

    captured = capsys.readouterr()
    report_text = report_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert report_path.exists()
    assert "Issues found: 6" in captured.out
    assert "Status: Issues found" in captured.out
    assert "Issues found: 6" in report_text

def test_main_handles_missing_input_file(tmp_path, capsys):
    report_path = tmp_path / "validation_report.txt"

    exit_code = main(
        "data/does_not_exist.csv",
        str(report_path),
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Input file not found" in captured.out
    assert not report_path.exists()