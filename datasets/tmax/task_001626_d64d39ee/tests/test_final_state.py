# test_final_state.py

import os
import csv
import math
import unicodedata
import pytest

PROCESSED_LOGS_PATH = "/home/user/processed_logs.csv"
RAW_LOGS_PATH = "/home/user/raw_logs.txt"

def test_processed_logs_exists():
    assert os.path.exists(PROCESSED_LOGS_PATH), f"Output file {PROCESSED_LOGS_PATH} was not created."
    assert os.path.isfile(PROCESSED_LOGS_PATH), f"{PROCESSED_LOGS_PATH} is not a file."

def test_processed_logs_format_and_content():
    assert os.path.exists(PROCESSED_LOGS_PATH), "Processed logs file is missing."

    with open(PROCESSED_LOGS_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty.")

        expected_header = ["timestamp", "metric_name", "metric_value", "message"]
        assert header == expected_header, f"Expected header {expected_header}, got {header}"

        rows = list(reader)

    assert len(rows) == 8, f"Expected exactly 8 rows in the output CSV, but found {len(rows)}."

    timestamps = [row[0] for row in rows]
    messages = [row[3] for row in rows]

    # Check Math Constraint (L2 > 5.0)
    assert '2023-10-01 10:00:00' not in timestamps, "Log entry with L2 norm == 5.0 was not filtered out."
    assert '2023-10-01 10:05:00' not in timestamps, "Log entry with L2 norm == 3.0 was not filtered out."
    assert '2023-10-01 10:20:00' not in timestamps, "Log entry with L2 norm == 3.0 was not filtered out."

    # Check Unicode Normalization and whitespace stripping
    assert "ff ligature test" in messages, "Ligature 'ﬀ' was not normalized to 'ff' using NFKC."
    assert "A bad string" in messages, "Fraktur '𝔄' was not normalized to 'A' or whitespace was not stripped."

    # Check Wide-Long Format Reshaping
    ts_101000_rows = [r for r in rows if r[0] == '2023-10-01 10:10:00']
    assert len(ts_101000_rows) == 3, f"Expected 3 rows for timestamp 10:10:00, got {len(ts_101000_rows)}"

    ts_102500_rows = [r for r in rows if r[0] == '2023-10-01 10:25:00']
    assert len(ts_102500_rows) == 2, f"Expected 2 rows for timestamp 10:25:00, got {len(ts_102500_rows)}"

    # Check specific row data for correctness
    # For 10:25:00, metrics a=5.0, b=5.0
    metrics_102500 = {(r[1], float(r[2])) for r in ts_102500_rows}
    assert metrics_102500 == {('a', 5.0), ('b', 5.0)}, f"Metrics for 10:25:00 are incorrect: {metrics_102500}"