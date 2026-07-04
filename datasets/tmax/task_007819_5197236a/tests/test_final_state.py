# test_final_state.py
import os
import re
import pytest

def test_results_file_exists():
    """Test that the results.txt file was created."""
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"The file {results_path} does not exist. Did you run the compiled executable and redirect standard output to it?"

def test_results_content():
    """Test that results.txt contains the correct regularized fitted values."""
    results_path = "/home/user/results.txt"
    with open(results_path, 'r') as f:
        content = f.read().strip()

    # Use regular expressions to allow for minor spacing differences, but exact precision matching
    expected_domain1 = r"Domain 1:\s*a=0\.7353,\s*b=0\.7647,\s*c=-0\.1471"
    expected_domain2 = r"Domain 2:\s*a=0\.9655,\s*b=0\.9655,\s*c=0\.4138"

    assert re.search(expected_domain1, content), f"Domain 1 results are incorrect or missing in results.txt.\nExpected to match: {expected_domain1}\nActual content:\n{content}"
    assert re.search(expected_domain2, content), f"Domain 2 results are incorrect or missing in results.txt.\nExpected to match: {expected_domain2}\nActual content:\n{content}"

def test_cpp_code_modified():
    """Check that the C++ code was actually modified to add the L2 penalty."""
    cpp_path = "/home/user/fit_plane.cpp"
    assert os.path.isfile(cpp_path), f"The file {cpp_path} is missing."

    with open(cpp_path, 'r') as f:
        content = f.read()

    # Check for evidence of adding to the diagonal
    # e.g., XtX[0][0] += 1.0 or XtX[i][i] += 1
    # We will just verify that the word 'NaN' is no longer the only outcome for Domain 2,
    # but more strictly, we look for '1.0' or '1' being added to the diagonal elements.
    assert re.search(r"XtX\[0\]\[0\]\s*\+=\s*1", content) or re.search(r"XtX\[i\]\[i\]\s*\+=\s*1", content) or re.search(r"XtX\[1\]\[1\]\s*\+=\s*1", content) or "1.0" in content, \
        "Could not find evidence of Ridge Regression (adding 1.0 to the diagonal of XtX) in fit_plane.cpp."