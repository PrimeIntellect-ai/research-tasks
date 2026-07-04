# test_final_state.py

import os
import pytest

def test_valid_samples_log():
    log_path = "/home/user/valid_samples.log"
    assert os.path.isfile(log_path), f"Output log file is missing: {log_path}"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_data = {
        "sample_1.csv": 0.016641,
        "sample_10.csv": 0.025409,
        "sample_3.csv": 0.014238,
        "sample_4.csv": 0.028911,
        "sample_6.csv": 0.012586,
        "sample_7.csv": 0.029462,
        "sample_9.csv": 0.008906
    }

    expected_files = sorted(expected_data.keys())
    actual_files = []

    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Invalid line format in log: '{line}'"
        filename, val_str = parts[0], parts[1]

        assert filename in expected_data, f"Unexpected file in log (or KL div should have been >= 0.15): {filename}"

        try:
            val = float(val_str)
        except ValueError:
            pytest.fail(f"Could not parse KL divergence as float: {val_str}")

        expected_val = expected_data[filename]
        assert abs(val - expected_val) < 0.001, f"KL divergence for {filename} is {val}, expected ~{expected_val}"

        actual_files.append(filename)

    assert actual_files == expected_files, f"Log file is not sorted alphabetically or missing files. Expected {expected_files}, got {actual_files}"