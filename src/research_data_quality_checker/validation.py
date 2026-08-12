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