# test_final_state.py

import os
import math

def test_pipeline_script_exists():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"Pipeline script is missing at {path}."

def test_cpp_processor_exists():
    path = "/home/user/process_logs.cpp"
    assert os.path.isfile(path), f"C++ source file is missing at {path}."

def test_processed_logs_exists():
    path = "/home/user/processed_logs.csv"
    assert os.path.isfile(path), f"Final output file is missing at {path}."

def test_processed_logs_content():
    path = "/home/user/processed_logs.csv"
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 6, f"Expected exactly 6 lines in {path}, but found {len(lines)}."

    expected_values = {
        0: -1.4638501,
        1: -0.8783100,
        2: -0.2927700,
        3: 0.2927700,
        4: 0.8783100,
        5: 1.4638501
    }

    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Line '{line}' is not in 'timestamp,normalized_value' format."

        try:
            t = int(parts[0])
            val = float(parts[1])
        except ValueError:
            assert False, f"Could not parse timestamp as int and value as float from line '{line}'."

        assert t in expected_values, f"Unexpected timestamp '{t}' found."

        # Check if the string representation has exactly 4 decimal places
        if '.' in parts[1]:
            decimals = len(parts[1].split('.')[1])
            assert decimals == 4, f"Value '{parts[1]}' does not have exactly 4 decimal places."
        else:
            assert False, f"Value '{parts[1]}' does not have exactly 4 decimal places."

        expected_val = expected_values[t]

        # Allow tolerance for standard rounding or half-to-even rounding
        diff = abs(val - expected_val)
        assert diff < 0.0002, f"Value at t={t} is {val}, expected approximately {expected_val:.4f}."