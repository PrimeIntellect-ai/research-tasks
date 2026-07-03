# test_final_state.py

import os
import pytest

RAW_DATA_PATH = "/home/user/raw_config.csv"
CLEAN_DATA_PATH = "/home/user/clean_config.csv"

def test_clean_config_exists():
    assert os.path.isfile(CLEAN_DATA_PATH), f"Output file {CLEAN_DATA_PATH} is missing."

def test_clean_config_content():
    # Read and process raw data to derive expected output
    assert os.path.isfile(RAW_DATA_PATH), f"Input file {RAW_DATA_PATH} is missing."

    records = {}
    with open(RAW_DATA_PATH, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 3:
                ts_str, param, val_str = parts[0], parts[1], parts[2]
                if param.lower() == 'max_workers':
                    ts = int(ts_str)
                    val = int(val_str)
                    if ts not in records or val > records[ts]:
                        records[ts] = val

    if not records:
        pytest.fail("No valid max_workers records found in raw data.")

    min_ts = min(records.keys())
    max_ts = max(records.keys())

    expected_lines = ["timestamp,param_name,value,delta"]

    current_val = None
    prev_val = None

    for ts in range(min_ts, max_ts + 10, 10):
        if ts in records:
            current_val = records[ts]
        # Forward fill: current_val remains the same if ts not in records

        if prev_val is None:
            delta = 0
        else:
            delta = current_val - prev_val

        expected_lines.append(f"{ts},max_workers,{current_val},{delta}")
        prev_val = current_val

    expected_content = "\n".join(expected_lines) + "\n"

    with open(CLEAN_DATA_PATH, 'r') as f:
        actual_content = f.read()

    # Normalize line endings
    actual_lines = [line.strip() for line in actual_content.strip().split('\n') if line.strip()]
    expected_lines_clean = [line.strip() for line in expected_content.strip().split('\n') if line.strip()]

    assert actual_lines == expected_lines_clean, f"Content of {CLEAN_DATA_PATH} does not match expected output.\nExpected:\n{expected_content}\nActual:\n{actual_content}"