# test_final_state.py

import os
import math

def test_results_csv_exists():
    path = "/home/user/results.csv"
    assert os.path.isfile(path), f"File {path} does not exist. Did you save the output?"

def test_results_csv_line_count():
    path = "/home/user/results.csv"
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 1000, f"Expected exactly 1000 lines in results.csv, but found {len(lines)}."

def test_no_nan_in_results():
    path = "/home/user/results.csv"
    with open(path, 'r') as f:
        for i, line in enumerate(f, 1):
            assert "NaN" not in line and "nan" not in line.lower(), f"Line {i} contains NaN: {line.strip()}"

def test_data_783_stddev():
    path = "/home/user/results.csv"
    found = False
    with open(path, 'r') as f:
        for line in f:
            if "data_783.txt" in line:
                found = True
                parts = line.strip().split(',')
                assert len(parts) == 2, f"Malformed line for data_783.txt: {line.strip()}"
                try:
                    stddev = float(parts[1])
                except ValueError:
                    assert False, f"Could not parse stddev as float for data_783.txt: {parts[1]}"

                # Population stddev of [0.1, 0.2, 0.1, 0.3, 0.2] is approx 0.074833
                assert math.isclose(stddev, 0.07483314773547883, rel_tol=1e-2), f"Incorrect stddev for data_783.txt. Expected ~0.074833, got {stddev}"
    assert found, "Output for data_783.txt not found in results.csv"

def test_data_402_stddev():
    path = "/home/user/results.csv"
    found = False
    with open(path, 'r') as f:
        for line in f:
            if "data_402.txt" in line:
                found = True
                parts = line.strip().split(',')
                assert len(parts) == 2, f"Malformed line for data_402.txt: {line.strip()}"
                try:
                    stddev = float(parts[1])
                except ValueError:
                    assert False, f"Could not parse stddev as float for data_402.txt: {parts[1]}"

                # Population stddev of [1.5, 1.7] is 0.1
                assert math.isclose(stddev, 0.1, rel_tol=1e-2), f"Incorrect stddev for data_402.txt. Expected 0.1, got {stddev}"
    assert found, "Output for data_402.txt not found in results.csv"

def test_executable_exists():
    path = "/home/user/processor"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile the code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."