# test_final_state.py

import os
import csv
import re
from collections import defaultdict
import pytest

SUMMARY_CSV = "/home/user/summary.csv"
LOGS_FILE = "/home/user/data/logs.jsonl"

def get_expected_summary():
    counts = defaultdict(int)
    with open(LOGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            ts_match = re.search(r'"ts":\s*"([^"]+)"', line)
            type_match = re.search(r'"type":\s*"([^"]+)"', line)
            if ts_match and type_match:
                ts = ts_match.group(1)
                etype = type_match.group(1)
                # Truncate to hour: e.g., 2023-01-01T14:32:01Z -> 2023-01-01T14:00:00Z
                hour = ts[:14] + "00:00Z"
                counts[(hour, etype)] += 1
            else:
                pytest.fail(f"Could not extract ts and type from line: {line}")

    sorted_keys = sorted(counts.keys())
    expected = []
    for k in sorted_keys:
        expected.append([k[0], k[1], str(counts[k])])
    return expected

def test_summary_csv_exists():
    assert os.path.exists(SUMMARY_CSV), f"Output file {SUMMARY_CSV} does not exist."
    assert os.path.isfile(SUMMARY_CSV), f"{SUMMARY_CSV} is not a file."

def test_summary_csv_content():
    assert os.path.exists(SUMMARY_CSV), f"Output file {SUMMARY_CSV} does not exist."

    with open(SUMMARY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"{SUMMARY_CSV} is empty.")

        assert header == ['hour', 'type', 'count'], f"Header is incorrect. Expected ['hour', 'type', 'count'], got {header}"

        student_rows = list(reader)

    expected_rows = get_expected_summary()

    assert len(student_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, but found {len(student_rows)}. Did you skip malformed lines?"

    for i, (student_row, expected_row) in enumerate(zip(student_rows, expected_rows)):
        assert student_row == expected_row, f"Row {i+2} mismatch. Expected {expected_row}, got {student_row}"

def test_total_count():
    assert os.path.exists(SUMMARY_CSV), f"Output file {SUMMARY_CSV} does not exist."

    total_count = 0
    with open(SUMMARY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_count += int(row['count'])

    assert total_count == 10000, f"Expected total count of 10000 events, but got {total_count}. Malformed lines must be repaired and counted, not skipped."