# test_final_state.py

import os
import csv
import pytest

CLEANED_CSV = '/home/user/cleaned.csv'
DROPPED_LOG = '/home/user/dropped.log'

def test_files_exist():
    assert os.path.isfile(CLEANED_CSV), f"{CLEANED_CSV} does not exist."
    assert os.path.isfile(DROPPED_LOG), f"{DROPPED_LOG} does not exist."

def test_dropped_log_content():
    expected_dropped = set()
    for i in range(1, 10001):
        if i % 73 == 0 or i % 191 == 0:
            expected_dropped.add(str(i))

    with open(DROPPED_LOG, 'r', encoding='utf-8') as f:
        dropped_ids = [line.strip() for line in f if line.strip()]

    assert len(dropped_ids) == len(expected_dropped), f"Expected {len(expected_dropped)} dropped IDs, found {len(dropped_ids)}."
    assert set(dropped_ids) == expected_dropped, "The dropped IDs do not match the expected malformed rows."

def test_cleaned_csv_content_and_order():
    with open(CLEANED_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['id', 'date', 'text'], "Header in cleaned.csv is incorrect."

        rows = list(reader)

    assert len(rows) == 9812, f"Expected 9812 cleaned rows, found {len(rows)}."

    previous_id = 0
    for row in rows:
        assert len(row) == 3, f"Row does not have exactly 3 columns: {row}"
        current_id = int(row[0])
        assert current_id > previous_id, "Rows are not strictly ordered by id ascending."
        previous_id = current_id

        # Check decoding
        text = row[2]
        assert "\\u" not in text, f"Found literal unicode escape in text: {text}"
        if current_id % 2 == 0:
            assert "café" in text, f"Expected 'café' in text, got: {text}"
            assert "☃" in text, f"Expected '☃' (snowman) in text, got: {text}"