def _format_value(value: str | int | None) -> str:
    if value is None:
        return "-"

    if isinstance(value, str) and value.strip() == "":
        return "<empty>"

    return str(value)

def build_terminal_summary(
        file_name: str,
        record_count: int,
        findings: list[dict[str, str | int | None]],
        report_path: str,
) -> str:
    if findings:
        status = "Issues found"
    else:
        status = "No issues found"

    return (
        "Research Data Quality Checker\n"
        f"File: {file_name}\n"
        f"Records checked: {record_count}\n"
        f"Issues found: {len(findings)}\n"
        f"Status: {status}\n"
        f"Report: {report_path}"
    )

def build_text_report(
        file_name: str,
        record_count: int,
        findings: list[dict[str, str | int | None]],
) -> str:
    if findings:
        status = "Issues found"
    else:
        status = "No issues found"

    lines = [
        "Research Data Quality Report",
        "============================",
        f"File: {file_name}",
        f"Records checked: {record_count}",
        f"Issues found: {len(findings)}",
        f"Status: {status}",
        "",
    ]

    if not findings:
        lines.append("No data quality issues found.")
        return "\n".join(lines)

    lines.extend(
        [
            "Findings",
            "--------",
        ]
    )

    for index, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"{index}. Type: {finding['type']}",
                f"   Row: {_format_value(finding['row_number'])}",
                (
                    "   Measurement ID: "
                    f"{_format_value(finding['measurement_id'])}"
                ),
                f"   Column: {_format_value(finding['column'])}",
                f"   Value: {_format_value(finding['value'])}",
                f"   Description: {finding['description']}",
                "",
            ]
        )
    return "\n".join(lines)

def write_text_report(
        report_path: str,
        report_text: str,
) -> None:
    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as report_file:
        report_file.write(report_text)