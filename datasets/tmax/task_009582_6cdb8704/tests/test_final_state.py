# test_final_state.py
import json
import os
import math
import pytest

SUMMARY_PATH = "/home/user/output/summary.json"
LOG_PATH = "/home/user/output/pipeline.log"

def test_summary_exists():
    assert os.path.isfile(SUMMARY_PATH), f"Summary file {SUMMARY_PATH} is missing. Make sure the script creates it."

def test_summary_content():
    with open(SUMMARY_PATH, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {SUMMARY_PATH} is not valid JSON.")

    expected_summary = {
        "electronics": 3.67,
        "home": 3.5,
        "garden": 3.0,
        "toys": 4.5
    }

    for category, expected_val in expected_summary.items():
        assert category in summary, f"Category '{category}' missing from summary."
        val = summary[category]
        assert isinstance(val, (int, float)), f"Value for '{category}' should be a number, got {type(val).__name__}."
        assert math.isclose(val, expected_val, abs_tol=0.01), \
            f"Mismatch in {category}: expected ~{expected_val}, got {val}"

    # Also check that there are no extra unexpected categories
    extra_keys = set(summary.keys()) - set(expected_summary.keys())
    assert not extra_keys, f"Found unexpected categories in summary: {extra_keys}"

def test_pipeline_log_exists():
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} is missing. Ensure the pipeline creates it."

def test_pipeline_log_content():
    with open(LOG_PATH, 'r') as f:
        log_lines = [line.strip() for line in f if line.strip()]

    expected_logs = [
        "[INFO] Processed batch1.csv: 4 records",
        "[INFO] Processed batch2.json: 3 records",
        "[INFO] Processed batch3.csv: 2 records"
    ]

    assert len(log_lines) == len(expected_logs), \
        f"Expected {len(expected_logs)} log entries, but got {len(log_lines)}."

    assert log_lines == expected_logs, \
        f"Log file contents do not match expected output or are not sorted properly.\nExpected: {expected_logs}\nGot: {log_lines}"