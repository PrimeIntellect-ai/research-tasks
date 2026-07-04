# test_final_state.py
import os
import re
import pytest

def test_aggregate_sh_fixed():
    """Check if aggregate.sh exists, is executable, and contains a sort command."""
    file_path = "/home/user/mc_sim/aggregate.sh"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

    with open(file_path, "r") as f:
        content = f.read()

    # Check that sort is used in the pipeline
    assert re.search(r'\bsort\b', content), "aggregate.sh does not seem to use 'sort' to order the intermediate outputs."

def test_averaged_signal_exists():
    """Check if averaged_signal.txt was generated."""
    file_path = "/home/user/mc_sim/averaged_signal.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run aggregate.sh?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    values = content.split(',')
    assert len(values) == 100, f"Expected 100 values in averaged_signal.txt, found {len(values)}."

def test_analyze_sh_exists_and_executable():
    """Check if analyze.sh exists and is executable."""
    file_path = "/home/user/mc_sim/analyze.sh"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_svd_top3_output():
    """Check if svd_top3.txt contains the correct singular values rounded to 4 decimal places."""
    file_path = "/home/user/mc_sim/svd_top3.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run analyze.sh?"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in svd_top3.txt, found {len(lines)}."

    expected_values = ["119.2941", "36.3150", "33.6062"]
    for i, (actual, expected) in enumerate(zip(lines, expected_values)):
        assert actual == expected, f"Line {i+1} in svd_top3.txt is '{actual}', expected '{expected}'."