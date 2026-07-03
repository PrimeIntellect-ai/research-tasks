# test_final_state.py

import os
import pytest
import stat

def test_script_exists_and_executable():
    """Test that the script exists and is executable."""
    script_path = "/home/user/compare_matrices.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), f"Script {script_path} is not executable."

def test_report_exists_and_correct():
    """Test that the report exists and has the correct output."""
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "Algorithm: qr, Max Diff: 0.045",
        "Algorithm: svd, Max Diff: 0.015",
        "Algorithm: lu, Max Diff: 0.002",
        "Algorithm: cholesky, Max Diff: 0"
    ]

    assert len(lines) == len(expected), f"Expected {len(expected)} lines in the report, but got {len(lines)}."

    for i, (act, exp) in enumerate(zip(lines, expected)):
        assert act == exp, f"Line {i+1} mismatch. Expected '{exp}', got '{act}'."