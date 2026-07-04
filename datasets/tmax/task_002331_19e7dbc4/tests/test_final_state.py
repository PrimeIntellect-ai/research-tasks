# test_final_state.py

import os
import csv
import zlib
import pytest

def tmr_encode(data: bytes) -> bytes:
    return bytes(b for b in data for _ in range(3))

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    # RapidCheck success usually outputs "OK, passed"
    assert "OK, passed" in content or "success" in content.lower(), f"RapidCheck success message not found in {log_path}."

def test_report_csv():
    csv_path = "/home/user/report.csv"
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    expected_rows = {
        "financials/2004.dat": "9c19b0bc",
        "engineering/blueprint.dat": "17f92023",
        "misc.dat": "36a8d3e2"
    }

    actual_rows = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                actual_rows[row[0].strip()] = row[1].strip().lower()

    for path, expected_crc in expected_rows.items():
        assert path in actual_rows, f"Missing entry for {path} in {csv_path}."
        assert actual_rows[path] == expected_crc, f"Incorrect CRC32 for {path}. Expected {expected_crc}, got {actual_rows[path]}."

def test_tmr_files():
    files_to_check = {
        "/home/user/data_lake/financials/2004.dat": b"CONFIDENTIAL_DATA_A",
        "/home/user/data_lake/engineering/blueprint.dat": b"PROJECT_BLUEPRINT_V1",
        "/home/user/data_lake/misc.dat": b"MISC_DATA_99"
    }

    for original_path, original_content in files_to_check.items():
        tmr_path = original_path + ".tmr"
        assert os.path.isfile(tmr_path), f"TMR encoded file {tmr_path} is missing."

        expected_tmr_content = tmr_encode(original_content)
        with open(tmr_path, "rb") as f:
            actual_tmr_content = f.read()

        assert actual_tmr_content == expected_tmr_content, f"Content of {tmr_path} does not match expected TMR encoding."