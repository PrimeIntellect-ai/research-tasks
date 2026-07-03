# test_final_state.py

import os
import math
import pytest

def test_preprocess_c_exists():
    """Verify that the C source code exists."""
    src_path = "/home/user/src/preprocess.c"
    assert os.path.isfile(src_path), f"Source file {src_path} is missing. You must write the C program."

def test_preprocess_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    bin_path = "/home/user/bin/preprocess"
    assert os.path.isfile(bin_path), f"Executable {bin_path} is missing. You must compile the program."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_prepared_data_correctness():
    """Verify that the prepared data file exists and contains the correct Z-score normalized values."""
    raw_data_path = "/home/user/raw_training_data.txt"
    prepared_data_path = "/home/user/prepared_data.txt"

    assert os.path.isfile(raw_data_path), f"Raw data file {raw_data_path} is missing."
    assert os.path.isfile(prepared_data_path), f"Prepared data file {prepared_data_path} is missing. Did you run the program on the raw data?"

    # Read raw data
    with open(raw_data_path, 'r') as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    raw_values = []
    for line in raw_lines:
        try:
            raw_values.append(float(line))
        except ValueError:
            pytest.fail(f"Could not parse '{line}' as a float in {raw_data_path}.")

    # Compute expected Z-scores
    n = len(raw_values)
    assert n > 0, "Raw data file is empty."

    mean = sum(raw_values) / n
    variance = sum((x - mean) ** 2 for x in raw_values) / n
    std_dev = math.sqrt(variance)

    expected_z_scores = []
    for x in raw_values:
        if std_dev == 0:
            expected_z_scores.append(0.0)
        else:
            expected_z_scores.append((x - mean) / std_dev)

    expected_lines = [f"{z:.6f}" for z in expected_z_scores]

    # Read prepared data
    with open(prepared_data_path, 'r') as f:
        prepared_lines = [line.strip() for line in f if line.strip()]

    assert len(prepared_lines) == len(expected_lines), (
        f"Prepared data has {len(prepared_lines)} lines, but expected {len(expected_lines)}."
    )

    for i, (prep, exp) in enumerate(zip(prepared_lines, expected_lines)):
        assert prep == exp, (
            f"Line {i+1} mismatch in {prepared_data_path}: expected {exp}, got {prep}."
        )