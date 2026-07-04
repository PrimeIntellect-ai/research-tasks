# test_final_state.py
import os
import re
import pytest

def test_pipeline_files_exist():
    """Verify that the user created the required source and script files."""
    assert os.path.isfile("/home/user/process.c"), "/home/user/process.c is missing"
    assert os.path.isfile("/home/user/pipeline.sh"), "/home/user/pipeline.sh is missing"

def test_output_files_exist():
    """Verify that the outputs of the C program were generated."""
    assert os.path.isfile("/home/user/Y.csv"), "/home/user/Y.csv is missing. Did the pipeline run and generate it?"
    assert os.path.isfile("/home/user/ci.txt"), "/home/user/ci.txt is missing. Did the pipeline run and generate it?"

def test_Y_csv_content():
    """Verify that Y.csv matches expected_Y.csv within a small tolerance."""
    with open("/home/user/Y.csv", "r") as f:
        y_lines = [line.strip() for line in f.readlines() if line.strip()]

    with open("/home/user/expected_Y.csv", "r") as f:
        expected_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(y_lines) == len(expected_lines), f"Y.csv row count ({len(y_lines)}) does not match expected ({len(expected_lines)})."

    for i, (y_line, exp_line) in enumerate(zip(y_lines, expected_lines)):
        y_vals = [float(v) for v in y_line.split(',')]
        exp_vals = [float(v) for v in exp_line.split(',')]

        assert len(y_vals) == len(exp_vals), f"Y.csv column count mismatch at row {i}."
        for j, (y_val, exp_val) in enumerate(zip(y_vals, exp_vals)):
            assert abs(y_val - exp_val) < 1e-3, f"Value mismatch at row {i}, col {j}: {y_val} != {exp_val}"

def test_ci_txt_content():
    """Verify that ci.txt has the correct format and values."""
    with open("/home/user/ci.txt", "r") as f:
        ci_content = f.read().strip()

    with open("/home/user/expected_ci.txt", "r") as f:
        expected_ci = f.read().strip()

    def parse_ci(text):
        match = re.search(r"Lower:\s*([-\d.]+),\s*Upper:\s*([-\d.]+)", text)
        if match:
            return float(match.group(1)), float(match.group(2))
        return None, None

    y_lower, y_upper = parse_ci(ci_content)
    exp_lower, exp_upper = parse_ci(expected_ci)

    assert y_lower is not None and y_upper is not None, f"ci.txt format is incorrect. Expected 'Lower: [val], Upper: [val]', got: '{ci_content}'"

    assert abs(y_lower - exp_lower) < 1e-3, f"Lower bound mismatch: {y_lower} != {exp_lower}"
    assert abs(y_upper - exp_upper) < 1e-3, f"Upper bound mismatch: {y_upper} != {exp_upper}"