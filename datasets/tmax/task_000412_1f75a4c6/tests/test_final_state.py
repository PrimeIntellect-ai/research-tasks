# test_final_state.py

import os
import csv
import pytest

OUTPUT_FILE = "/home/user/output/clean_events.csv"

def test_output_file_exists():
    """Test that the output CSV file exists."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing. Did the program run successfully?"

def test_output_file_is_utf8():
    """Test that the output file is valid UTF-8 encoded."""
    try:
        with open(OUTPUT_FILE, "rb") as f:
            content = f.read()
            content.decode("utf-8")
    except UnicodeDecodeError as e:
        pytest.fail(f"Output file is not valid UTF-8: {e}")

def test_output_file_content_and_sort():
    """Test that the output file has the correct deduplicated, sorted, and normalized content."""
    # Read the file as UTF-8
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output file is empty."

    # Check header
    header = rows[0]
    expected_header = ["event_id", "timestamp", "user_name", "action"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = rows[1:]

    # Check deduplication
    event_ids = [row[0] for row in data_rows]
    assert len(event_ids) == len(set(event_ids)), "Duplicate event_ids found in the output. Deduplication failed."

    # Check sorting: primarily by timestamp, secondarily by event_id
    sorted_data_rows = sorted(data_rows, key=lambda x: (x[1], x[0]))
    assert data_rows == sorted_data_rows, "Output data is not sorted correctly by timestamp and event_id."

    # Check exact expected rows
    expected_rows = [
        ["E101", "2023-10-01T10:00:00", "José", "login"],
        ["E102", "2023-10-01T10:01:00", "Bob", "click"],
        ["E103", "2023-10-01T10:02:00", "Müller", "purchase"],
        ["E104", "2023-10-01T10:04:00", "François", "login"],
        ["E105", "2023-10-01T10:05:00", "Alice", "logout"],
        ["E106", "2023-10-01T10:06:00", "Charlie", "click"],
        ["E107", "2023-10-01T10:08:00", "Diana", "purchase"],
        ["E108", "2023-10-01T10:10:00", "Björn", "logout"]
    ]

    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} records, got {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_source_code_exists():
    """Test that the C++ source code exists where expected."""
    assert os.path.isfile("/home/user/dedup_etl.cpp"), "Source file /home/user/dedup_etl.cpp is missing."

def test_executable_exists():
    """Test that the compiled executable exists."""
    assert os.path.isfile("/home/user/dedup_etl"), "Compiled executable /home/user/dedup_etl is missing."
    assert os.access("/home/user/dedup_etl", os.X_OK), "File /home/user/dedup_etl is not executable."