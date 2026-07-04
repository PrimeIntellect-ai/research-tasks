# test_final_state.py
import os
import csv
import json
import subprocess
import pytest
from datetime import datetime

SUMMARY_CSV = "/home/user/output/user_summary.csv"
LOGS_PARQUET = "/home/user/output/cleaned_logs.parquet"

def get_parquet_data(filepath):
    """
    Reads a Parquet file by shelling out to Python with pandas,
    returning a list of dictionaries. This avoids importing third-party
    libraries directly in the test suite as per constraints.
    """
    code = f"""
import pandas as pd
import json
try:
    df = pd.read_parquet('{filepath}')
    df['timestamp'] = df['timestamp'].astype(str)
    print(df.to_json(orient='records'))
except Exception as e:
    import sys
    sys.exit(str(e))
"""
    result = subprocess.run(['python3', '-c', code], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Failed to read parquet file {filepath}. Error: {result.stderr.strip() or result.stdout.strip()}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Could not parse parquet data as JSON. Output was: {result.stdout}")

def test_output_directories_exist():
    assert os.path.exists("/home/user/output"), "Output directory /home/user/output does not exist."

def test_user_summary_csv():
    assert os.path.isfile(SUMMARY_CSV), f"Summary file {SUMMARY_CSV} is missing."

    with open(SUMMARY_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames is not None, "Summary CSV must have a header."

    # Check exact columns
    expected_cols = {"user_id", "app", "email"}
    actual_cols = set(reader.fieldnames)
    assert expected_cols.issubset(actual_cols), f"Summary CSV missing expected columns. Found: {actual_cols}"

    # Check data content
    summary_map = {row["user_id"]: row for row in rows}

    assert len(summary_map) == 3, f"Expected 3 unique users in summary, found {len(summary_map)}."

    # U100: 3 app, 1 email
    assert "U100" in summary_map, "User U100 missing from summary."
    assert int(summary_map["U100"]["app"]) == 3, "U100 app count should be 3."
    assert int(summary_map["U100"]["email"]) == 1, "U100 email count should be 1."

    # U101: 0 app, 2 email
    assert "U101" in summary_map, "User U101 missing from summary."
    assert int(summary_map["U101"]["app"]) == 0, "U101 app count should be 0."
    assert int(summary_map["U101"]["email"]) == 2, "U101 email count should be 2."

    # U102: 1 app, 0 email
    assert "U102" in summary_map, "User U102 missing from summary."
    assert int(summary_map["U102"]["app"]) == 1, "U102 app count should be 1."
    assert int(summary_map["U102"]["email"]) == 0, "U102 email count should be 0."

    # Check sorting
    user_ids = [row["user_id"] for row in rows]
    assert user_ids == sorted(user_ids), "Summary CSV must be sorted ascending by user_id."

def test_cleaned_logs_parquet():
    assert os.path.isfile(LOGS_PARQUET), f"Parquet file {LOGS_PARQUET} is missing."

    data = get_parquet_data(LOGS_PARQUET)
    assert len(data) == 7, f"Expected 7 total logs in parquet file, found {len(data)}."

    # Check columns
    expected_cols = {"timestamp", "user_id", "text", "source", "normalized_text", "rolling_msg_1h"}
    if data:
        actual_cols = set(data[0].keys())
        assert expected_cols.issubset(actual_cols), f"Parquet missing expected columns. Found: {actual_cols}"

    # Verify sorting: user_id ascending, then timestamp ascending
    for i in range(1, len(data)):
        prev, curr = data[i-1], data[i]
        assert prev["user_id"] <= curr["user_id"], "Parquet data not sorted by user_id ascending."
        if prev["user_id"] == curr["user_id"]:
            assert prev["timestamp"] <= curr["timestamp"], "Parquet data not sorted by timestamp ascending within user_id."

    # Verify U100 rolling counts and normalization
    u100_logs = [row for row in data if row["user_id"] == "U100"]
    assert len(u100_logs) == 4, f"Expected 4 logs for U100, found {len(u100_logs)}"

    rolling_vals = [int(row["rolling_msg_1h"]) for row in u100_logs]
    assert rolling_vals == [1, 2, 3, 2], f"Rolling values for U100 incorrect. Expected [1, 2, 3, 2], got {rolling_vals}"

    norm_text_0 = u100_logs[0]["normalized_text"]
    assert norm_text_0 == "hello my order failed", f"Normalization incorrect for first U100 log. Got: '{norm_text_0}'"

    # Verify U101 rolling counts
    u101_logs = [row for row in data if row["user_id"] == "U101"]
    assert len(u101_logs) == 2, f"Expected 2 logs for U101, found {len(u101_logs)}"

    rolling_vals_101 = [int(row["rolling_msg_1h"]) for row in u101_logs]
    assert rolling_vals_101 == [1, 1], f"Rolling values for U101 incorrect. Expected [1, 1], got {rolling_vals_101}"

    # Verify U102 rolling counts
    u102_logs = [row for row in data if row["user_id"] == "U102"]
    assert len(u102_logs) == 1, f"Expected 1 log for U102, found {len(u102_logs)}"
    assert int(u102_logs[0]["rolling_msg_1h"]) == 1, "Rolling value for U102 incorrect."