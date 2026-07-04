# test_final_state.py

import os
import csv
import pytest

def test_script_is_executable():
    script_path = "/home/user/process_logs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_normalized_configs_exists():
    output_path = "/home/user/normalized_configs.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_normalized_configs_content():
    output_path = "/home/user/normalized_configs.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_rows = [
        ["ServerID", "EpochTimestamp", "ConfigKey", "NotesLength"],
        ["srv-C", "1698170400", "feature_flag_x", "7"],
        ["srv-A", "1698273000", "max_connections", "47"],
        ["srv-B", "1698273000", "cache_size", "101"],
        ["srv-C", "1698273000", "worker_threads", "12"],
        ["srv-A", "1698340500", "timeout", "10"],
        ["srv-B", "1698393600", "log_level", "12"]
    ]

    with open(output_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_normalized_configs_sorting():
    output_path = "/home/user/normalized_configs.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    # Check that it's sorted by EpochTimestamp (asc), then ServerID (asc)
    try:
        sorted_data = sorted(data, key=lambda x: (int(x[1]), x[0]))
    except ValueError:
        pytest.fail("EpochTimestamp column contains non-integer values.")

    assert data == sorted_data, "The CSV rows are not correctly sorted by EpochTimestamp then ServerID."