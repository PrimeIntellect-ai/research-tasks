# test_final_state.py
import os
import csv
import json
import pytest

ARCHIVE_DIR = "/home/user/archive"

def test_archive_directory_exists():
    assert os.path.exists(ARCHIVE_DIR), f"Directory missing: {ARCHIVE_DIR}"
    assert os.path.isdir(ARCHIVE_DIR), f"Expected a directory, found something else: {ARCHIVE_DIR}"

def test_archive_files_exist_and_counts():
    file_001 = os.path.join(ARCHIVE_DIR, "archive_001.csv")
    file_002 = os.path.join(ARCHIVE_DIR, "archive_002.csv")
    file_003 = os.path.join(ARCHIVE_DIR, "archive_003.csv")
    file_004 = os.path.join(ARCHIVE_DIR, "archive_004.csv")

    assert os.path.exists(file_001), "archive_001.csv is missing."
    assert os.path.exists(file_002), "archive_002.csv is missing."
    assert os.path.exists(file_003), "archive_003.csv is missing."
    assert not os.path.exists(file_004), "archive_004.csv should not exist."

def test_csv_headers_and_content():
    expected_header = ["Timestamp", "Level", "ServerName", "Message"]

    files_to_check = [
        ("archive_001.csv", 50),
        ("archive_002.csv", 50),
        ("archive_003.csv", 15)
    ]

    total_records = 0

    for filename, expected_count in files_to_check:
        filepath = os.path.join(ARCHIVE_DIR, filename)
        assert os.path.exists(filepath), f"{filename} is missing."

        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            assert header == expected_header, f"Header in {filename} does not match expected. Got: {header}"

            row_count = 0
            for row in reader:
                assert len(row) == 4, f"Row in {filename} does not have exactly 4 columns: {row}"

                level = row[1]
                server_name = row[2]

                assert level in ["ERROR", "CRITICAL"], f"Invalid level '{level}' found in {filename}."
                assert server_name != "S4", f"Raw ServerID 'S4' found in {filename}, should be 'UNKNOWN'."
                if server_name not in ["Alpha_Node", "Beta_Node", "Gamma_Node"]:
                    assert server_name == "UNKNOWN", f"Unexpected ServerName '{server_name}' found in {filename}."

                row_count += 1
                total_records += 1

            assert row_count == expected_count, f"Expected {expected_count} records in {filename}, got {row_count}."

    assert total_records == 115, f"Expected exactly 115 error/critical records total, got {total_records}."