REQUIRED_COLUMNS = (
    "measurement_id",
    "station_id",
    "measurement_date",
    "temperature_c",
    "humidity_percent",
    "pressure_hpa",
)

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