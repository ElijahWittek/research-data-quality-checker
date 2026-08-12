import csv


def read_csv_file(
        file_path: str,
) -> tuple[list[str], list[dict[str, str]]]:
    with open(
        file_path,
        encoding="utf-8",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")

        columns = reader.fieldnames or []
        rows = list(reader)

    return columns, rows