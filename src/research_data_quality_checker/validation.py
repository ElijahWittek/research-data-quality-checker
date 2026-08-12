from datetime import date

REQUIRED_COLUMNS = (
    "measurement_id",
    "station_id",
    "measurement_date",
    "temperature_c",
    "humidity_percent",
    "pressure_hpa",
)

MEASUREMENT_RANGES = {
    "temperature_c": (-50.0, 60.0),
    "humidity_percent": (0.0, 100.0),
    "pressure_hpa": (850.0, 1100.0),
}

def get_missing_required_columns(columns: list[str]) -> list[str]:
    missing_columns = []

    for required_column in REQUIRED_COLUMNS:
        if required_column not in columns:
            missing_columns.append(required_column)

    return missing_columns

def is_missing_value(value: str) -> bool:
    return value.strip() == ""

def get_missing_required_values(row: dict[str, str]) -> list[str]:
    missing_values = []

    for required_column in REQUIRED_COLUMNS:
        if required_column in row and is_missing_value(row[required_column]):
            missing_values.append(required_column)

    return missing_values

def is_positive_integer(value: str) -> bool:
    try:
        number = int(value)
    except ValueError:
        return False

    return number > 0

def is_decimal_number(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False

    return True

def is_valid_date(value: str) -> bool:
    try:
        parsed_date = date.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False

    return parsed_date.strftime("%Y-%m-%d") == value

def get_duplicate_measurement_ids(measurement_ids: list[str]) -> list[str]:
    seen_ids = set()
    duplicate_ids = []

    for measurement_id in measurement_ids:
        if measurement_id in seen_ids and measurement_id not in duplicate_ids:
            duplicate_ids.append(measurement_id)
        else:
            seen_ids.add(measurement_id)

    return duplicate_ids

def is_within_range(
        value: str,
        lower_bound: float,
        upper_bound: float,
) -> bool:
    number = float(value)

    return lower_bound <= number <= upper_bound

def get_out_of_range_values(row: dict[str, str]) -> list[str]:
    out_of_range_values = []

    for column, (lower_bound, upper_bound) in MEASUREMENT_RANGES.items():
        if column not in row:
            continue

        value = row[column]

        if is_missing_value(value) or not is_decimal_number(value):
            continue

        if not is_within_range(value, lower_bound, upper_bound):
            out_of_range_values.append(column)

    return out_of_range_values

def validate_row(
        row: dict[str, str],
        row_number: int,
) -> list[dict[str, str | int | None]]:
    findings = []

    measurement_id = row.get("measurement_id")

    if measurement_id is not None and is_missing_value(measurement_id):
        measurement_id = None

    missing_values = get_missing_required_values(row)

    for column in missing_values:
        findings.append(
            {
                "type": "missing_value",
                "row_number": row_number,
                "measurement_id": measurement_id,
                "column": column,
                "value": row[column],
                "discription": "Required value is missing.",
            }
        )

    if "measurement_id" in row and "measurement_id" not in missing_values:
        value = row["measurement_id"]

        if not is_positive_integer(value):
            findings.append(
                {
                    "type": "invalid_number",
                    "row_number": row_number,
                    "measurement_id": measurement_id,
                    "column": "measurement_id",
                    "value": value,
                    "discription": "Value must be a positive integer.",
                }
            )

    if "measurement_date" in row and "measurement_date" not in missing_values:
        value = row["measurement_date"]

        if not is_valid_date(value):
            findings.append(
                {
                    "type": "invalid_date",
                    "row_number": row_number,
                    "measurement_id": measurement_id,
                    "column": "measurement_date",
                    "value": value,
                    "discription": "Value must be a valid date in YYYY-MM-DD format.",
                }
            )

    for column, (lower_bound, upper_bound) in MEASUREMENT_RANGES.items():
        if column not in row or column in missing_values:
            continue

        value = row[column]

        if not is_decimal_number(value):
            findings.append(
                {
                    "type": "invalid_number",
                    "row_number": row_number,
                    "measurement_id": measurement_id,
                    "column": column,
                    "value": value,
                    "discription": "Value must be a valid decimal number.",
                }
            )
            continue

        if not is_within_range(value, lower_bound, upper_bound):
            findings.append(
                {
                    "type": "out_of_range",
                    "row_number": row_number,
                    "measurement_id": measurement_id,
                    "column": column,
                    "value": value,
                    "discription": (
                        f"Value must be between {lower_bound} "
                        f"and {upper_bound}, inclusive."
                    ),
                }
            )

    return findings

def validate_dataset(
        columns: list[str],
        rows: list[dict[str, str]],
) -> list[dict[str, str | int | None]]:
    findings = []

    missing_columns = get_missing_required_columns(columns)

    for column in missing_columns:
        findings.append(
            {
                "type": "missing_column",
                "row_number": None,
                "measurement_id": None,
                "column": column,
                "value": None,
                "description": "Required column is missing.",
            }
        )

    seen_measurement_ids = set()

    for row_number, row in enumerate(rows, start=2):
        findings.extend(validate_row(row, row_number))

        measurement_id = row.get("measurement_id")

        if (
            measurement_id is None
            or is_missing_value(measurement_id)
            or not is_positive_integer(measurement_id)
        ):
            continue

        if measurement_id in seen_measurement_ids:
            findings.append(
                {
                    "type": "duplicate_measurement_id",
                    "row_number": row_number,
                    "measurement_id": measurement_id,
                    "column": "measurement_id",
                    "value": measurement_id,
                    "description": "Measurement ID has already occurred.",
                }
            )
        else:
            seen_measurement_ids.add(measurement_id)

    return findings