# test_final_state.py
import os
import csv

def test_output_csv_exists():
    path = '/home/user/customer_revenue_rank.csv'
    assert os.path.isfile(path), f"The output CSV file {path} does not exist. Did you run the script?"

def test_output_csv_content():
    path = '/home/user/customer_revenue_rank.csv'
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The output CSV is empty."

    header = rows[0]
    expected_header = ['customer_id', 'total_revenue', 'revenue_rank']
    assert header == expected_header, f"Expected header {expected_header}, but got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected exactly 3 data rows (excluding Charlie who has no orders), but got {len(data_rows)}."

    # Parse rows to handle formatting differences (e.g., "50" vs "50.0")
    parsed_rows = []
    for row in data_rows:
        assert len(row) == 3, f"Expected 3 columns per row, got {len(row)} in row: {row}"
        parsed_rows.append((int(row[0]), float(row[1]), int(row[2])))

    expected_rows = [
        (2, 50.0, 1),
        (4, 50.0, 1),
        (1, 45.0, 3)
    ]

    assert parsed_rows == expected_rows, (
        f"Output CSV data does not match expected results.\n"
        f"Expected: {expected_rows}\n"
        f"Got:      {parsed_rows}\n"
        f"Ensure you are ordering by revenue_rank ASC, then customer_id ASC, and using RANK()."
    )