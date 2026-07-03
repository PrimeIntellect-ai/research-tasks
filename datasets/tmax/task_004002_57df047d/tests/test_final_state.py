# test_final_state.py
import os
import math
import pytest

POOLED_FILE = "/home/user/pooled_preds.csv"
BOOTSTRAP_FILE = "/home/user/bootstrap_sample.csv"
REPORT_FILE = "/home/user/report.txt"

def test_pooled_preds_file():
    assert os.path.exists(POOLED_FILE), f"File not found: {POOLED_FILE}"

    with open(POOLED_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 15, f"Expected exactly 15 lines in {POOLED_FILE}, but got {len(lines)}"

    valid_patterns = {"0,0", "0,1", "1,0", "1,1"}
    for i, line in enumerate(lines):
        assert line in valid_patterns, f"Invalid data on line {i+1} of {POOLED_FILE}: '{line}'. Only '0,0', '0,1', '1,0', and '1,1' are allowed."

def test_bootstrap_sample_file():
    assert os.path.exists(BOOTSTRAP_FILE), f"File not found: {BOOTSTRAP_FILE}"

    with open(BOOTSTRAP_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 500, f"Expected exactly 500 lines in {BOOTSTRAP_FILE}, but got {len(lines)}"

    valid_patterns = {"0,0", "0,1", "1,0", "1,1"}
    for i, line in enumerate(lines):
        assert line in valid_patterns, f"Invalid data on line {i+1} of {BOOTSTRAP_FILE}: '{line}'. Only '0,0', '0,1', '1,0', and '1,1' are allowed."

def test_evaluate_and_report():
    assert os.path.exists(BOOTSTRAP_FILE), f"Cannot evaluate accuracy because {BOOTSTRAP_FILE} is missing."
    assert os.path.exists(REPORT_FILE), f"File not found: {REPORT_FILE}"

    with open(BOOTSTRAP_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"{BOOTSTRAP_FILE} is empty, cannot compute accuracy."

    correct_count = 0
    for line in lines:
        parts = line.split(',')
        if len(parts) == 2 and parts[0] == parts[1]:
            correct_count += 1

    expected_accuracy = correct_count / len(lines)

    with open(REPORT_FILE, 'r') as f:
        report_content = f.read().strip()

    try:
        reported_accuracy = float(report_content)
    except ValueError:
        pytest.fail(f"Could not parse a float from {REPORT_FILE}. Content was: '{report_content}'")

    assert math.isclose(reported_accuracy, expected_accuracy, rel_tol=1e-5, abs_tol=1e-5), \
        f"Reported accuracy {reported_accuracy} does not match the expected accuracy {expected_accuracy} calculated from {BOOTSTRAP_FILE}."