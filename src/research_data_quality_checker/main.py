import sys
from pathlib import Path

from research_data_quality_checker.csv_reader import read_csv_file
from research_data_quality_checker.report import (
    build_terminal_summary,
    build_text_report,
    write_text_report,
)
from research_data_quality_checker.validation import validate_dataset

DEFAULT_REPORT_PATH = "validation_report.txt"


def main(
        file_path: str,
        report_path: str = DEFAULT_REPORT_PATH,
) -> int:
    try:
        columns, rows = read_csv_file(file_path)
    except FileNotFoundError:
        print(f"Error: Input file not found: {file_path}")
        return 1
    except (OSError, UnicodeError) as error:
        print(f"Error: Could not read input file: {error}")
        return 1

    findings = validate_dataset(columns, rows)

    file_name = Path(file_path).name

    report_text = build_text_report(
        file_name,
        len(rows),
        findings,
    )

    try:
        write_text_report(report_path, report_text)
    except OSError as error:
        print(f"Error: Could not write report: {error}")
        return 1

    summary = build_terminal_summary(
        file_name,
        len(rows),
        findings,
        report_path,
    )

    print(summary)

    return 0

def cli() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: research-data-quality-checker "
            "<csv-file>"
        )
        raise SystemExit(1)
    
    raise SystemExit(main(sys.argv[1]))

if __name__ == "__main__":
    cli()