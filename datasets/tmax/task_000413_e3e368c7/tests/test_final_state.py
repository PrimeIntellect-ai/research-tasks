# test_final_state.py

import os
import json
import csv
import struct
import pytest

BASE_DIR = "/home/user/backups"
CSV_PATH = os.path.join(BASE_DIR, "index.csv")
JSON_PATH = "/home/user/archive_summary.json"
C_FILE_PATH = "/home/user/archive_tool.c"

def get_expected_data():
    expected = []
    with open(CSV_PATH, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            backup_id = row["BackupID"]
            rel_path = row["RelativePath"]
            offset = int(row["HeaderOffset"])

            bin_path = os.path.join(BASE_DIR, rel_path)
            with open(bin_path, "rb") as bin_f:
                bin_f.seek(offset)
                header = bin_f.read(8)

            magic_bytes = header[0:4]
            magic_str = "".join(f"{b:02X}" for b in magic_bytes)

            timestamp = struct.unpack("<I", header[4:8])[0]

            expected.append({
                "BackupID": backup_id,
                "Magic": magic_str,
                "Timestamp": timestamp
            })
    return expected

def test_c_source_exists():
    assert os.path.isfile(C_FILE_PATH), f"C source file not found at {C_FILE_PATH}"

def test_json_output_exists():
    assert os.path.isfile(JSON_PATH), f"JSON output file not found at {JSON_PATH}"

def test_json_output_content():
    expected_data = get_expected_data()

    with open(JSON_PATH, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON output: {e}")

    assert isinstance(actual_data, list), "JSON output must be an array of objects."

    # Sort both lists by BackupID to ensure order doesn't fail the test
    actual_sorted = sorted(actual_data, key=lambda x: x.get("BackupID", ""))
    expected_sorted = sorted(expected_data, key=lambda x: x["BackupID"])

    assert len(actual_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} entries, found {len(actual_sorted)}"

    for actual, expected in zip(actual_sorted, expected_sorted):
        assert actual.get("BackupID") == expected["BackupID"], f"BackupID mismatch: expected {expected['BackupID']}, got {actual.get('BackupID')}"
        assert actual.get("Magic") == expected["Magic"], f"Magic mismatch for {expected['BackupID']}: expected {expected['Magic']}, got {actual.get('Magic')}"
        assert actual.get("Timestamp") == expected["Timestamp"], f"Timestamp mismatch for {expected['BackupID']}: expected {expected['Timestamp']}, got {actual.get('Timestamp')}"