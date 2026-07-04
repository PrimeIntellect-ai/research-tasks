# test_final_state.py

import os
import pytest

RAW_COVERAGE_PATH = "/home/user/raw_coverage.txt"
SORTED_COVERAGE_PATH = "/home/user/sorted_coverage.txt"
TOP100_SUM_PATH = "/home/user/top100_sum.txt"
EXPECTED_SUM_PATH = "/home/user/.expected_sum.txt"

def test_raw_coverage_exists_and_has_data():
    assert os.path.isfile(RAW_COVERAGE_PATH), f"File not found: {RAW_COVERAGE_PATH}"
    with open(RAW_COVERAGE_PATH, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 10050, f"Expected 10050 lines in {RAW_COVERAGE_PATH}, found {len(lines)}"
    # Check that they can be parsed as floats
    try:
        [float(x.strip()) for x in lines]
    except ValueError:
        pytest.fail(f"Not all lines in {RAW_COVERAGE_PATH} are valid floats.")

def test_sorted_coverage_is_sorted_descending():
    assert os.path.isfile(SORTED_COVERAGE_PATH), f"File not found: {SORTED_COVERAGE_PATH}"
    with open(SORTED_COVERAGE_PATH, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 10050, f"Expected 10050 lines in {SORTED_COVERAGE_PATH}, found {len(lines)}"

    try:
        values = [float(x.strip()) for x in lines]
    except ValueError:
        pytest.fail(f"Not all lines in {SORTED_COVERAGE_PATH} are valid floats.")

    # Check if sorted descending
    assert all(values[i] >= values[i+1] for i in range(len(values)-1)), f"The values in {SORTED_COVERAGE_PATH} are not strictly sorted in descending order."

def test_top100_sum_is_correct():
    assert os.path.isfile(TOP100_SUM_PATH), f"File not found: {TOP100_SUM_PATH}"
    assert os.path.isfile(EXPECTED_SUM_PATH), f"Setup file missing: {EXPECTED_SUM_PATH}"

    with open(EXPECTED_SUM_PATH, 'r') as f:
        expected_sum = f.read().strip()

    with open(TOP100_SUM_PATH, 'r') as f:
        actual_sum = f.read().strip()

    assert actual_sum == expected_sum, f"Expected sum {expected_sum}, but got {actual_sum} in {TOP100_SUM_PATH}"

    # Check formatting (exactly 4 decimal places)
    parts = actual_sum.split('.')
    assert len(parts) == 2, f"Sum {actual_sum} is not formatted correctly with a decimal point."
    assert len(parts[1]) == 4, f"Sum {actual_sum} must be formatted to exactly 4 decimal places."