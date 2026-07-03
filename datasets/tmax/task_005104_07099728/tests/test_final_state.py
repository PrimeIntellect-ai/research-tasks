# test_final_state.py

import os
import math
import pytest

def test_extractor_executable_exists():
    path = "/home/user/bin/extractor"
    assert os.path.isfile(path), f"Expected executable {path} to exist."
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."

def test_signal_csv_exists_and_valid():
    path = "/home/user/data/signal.csv"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 1024, f"Expected {path} to contain exactly 1024 lines, found {len(lines)}."

    # Check if first line is a float
    try:
        float(lines[0])
    except ValueError:
        pytest.fail(f"First line of {path} is not a valid float: {lines[0]}")

def test_rust_project_exists():
    cargo_path = "/home/user/processor/Cargo.toml"
    assert os.path.isfile(cargo_path), f"Expected Rust project Cargo.toml at {cargo_path}."

def test_processed_csv_exists_and_valid():
    path = "/home/user/data/processed.csv"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 1024, f"Expected {path} to contain exactly 1024 lines, found {len(lines)}."

    for i, line in enumerate(lines):
        # Check format: exactly 4 decimal places
        if '.' in line:
            decimals = len(line.split('.')[1])
            assert decimals == 4, f"Expected exactly 4 decimal places at index {i}, got {decimals} in '{line}'."
        else:
            pytest.fail(f"Expected floating point number with 4 decimal places at index {i}, got '{line}'.")

        t = i / 1024.0
        expected = math.sin(2 * math.pi * 10 * t)

        try:
            actual = float(line)
        except ValueError:
            pytest.fail(f"Invalid float at index {i}: {line}")

        assert abs(expected - actual) <= 1e-3, f"Mismatch at index {i}: expected {expected}, got {actual}"