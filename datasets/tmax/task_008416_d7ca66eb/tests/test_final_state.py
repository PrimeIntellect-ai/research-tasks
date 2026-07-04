# test_final_state.py

import os
import re
import pytest

def test_bootstrap_results_exists():
    file_path = "/home/user/bootstrap_results.txt"
    assert os.path.isfile(file_path), f"Error: {file_path} does not exist. Did you run your C++ program and generate the output?"

def test_bootstrap_results_content():
    file_path = "/home/user/bootstrap_results.txt"
    with open(file_path, "r") as f:
        content = f.read()

    # Check Valid rows
    assert "Valid rows: 11" in content, "Error: The number of valid rows is incorrect. Expected 'Valid rows: 11'."

    # Check Mean (should start with 86.6, as 86.64 is the exact expected value but we allow some flexibility)
    assert re.search(r"Mean:\s*86\.6", content), "Error: The overall mean is incorrect. Expected a value around 86.6X."

    # Check 95% CI format
    assert "95% CI:" in content, "Error: '95% CI:' not found in the output."
    assert re.search(r"95% CI:\s*\[\d+\.\d{2},\s*\d+\.\d{2}\]", content), "Error: The 95% CI format is incorrect. Expected '95% CI: [L.LL, U.UU]'."

def test_cpp_source_exists():
    file_path = "/home/user/bootstrap.cpp"
    assert os.path.isfile(file_path), f"Error: {file_path} does not exist. Make sure you saved your C++ code to this location."