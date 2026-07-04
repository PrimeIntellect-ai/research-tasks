# test_final_state.py
import os
import csv
import pytest

def test_output_file_exists():
    path = "/home/user/cleaned_product_stats.csv"
    assert os.path.isfile(path), f"Output file is missing: {path}"

def test_output_file_contents():
    path = "/home/user/cleaned_product_stats.csv"

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The output CSV is empty."

    headers = rows[0]
    expected_headers = ['product_id', 'review_count', 'avg_word_count']
    assert headers == expected_headers, f"Expected headers {expected_headers}, but got {headers}"

    data_rows = rows[1:]
    assert len(data_rows) == 4, f"Expected 4 data rows, but got {len(data_rows)}"

    # Parse and check values
    parsed_rows = []
    for row in data_rows:
        assert len(row) == 3, f"Row has incorrect number of columns: {row}"
        product_id, review_count, avg_word_count = row
        parsed_rows.append((product_id, int(review_count), float(avg_word_count)))

    expected_data = [
        ('p1', 2, 3.00),
        ('p3', 2, 1.50),
        ('p2', 1, 3.00),
        ('p4', 1, 5.00)
    ]

    for i, (actual, expected) in enumerate(zip(parsed_rows, expected_data)):
        assert actual[0] == expected[0], f"Row {i+1}: Expected product_id {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"Row {i+1}: Expected review_count {expected[1]}, got {actual[1]}"
        assert abs(actual[2] - expected[2]) < 1e-2, f"Row {i+1}: Expected avg_word_count {expected[2]}, got {actual[2]}"