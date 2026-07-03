# test_final_state.py

import os
import stat

def test_analyze_sh_exists_and_executable():
    """Test that analyze.sh exists and is executable."""
    script_path = '/home/user/analyze.sh'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_clean_values_txt_exists_and_valid():
    """Test that clean_values.txt was created and contains only valid numbers."""
    clean_path = '/home/user/clean_values.txt'
    assert os.path.exists(clean_path), f"The file {clean_path} was not created."

    with open(clean_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"{clean_path} is empty."

    for line in lines:
        try:
            val = float(line)
            assert -1000 <= val <= 1000, f"Value {val} in {clean_path} is outside the valid range [-1000, 1000]."
        except ValueError:
            assert False, f"Non-numeric value '{line}' found in {clean_path}."

def test_bootstrap_py_exists():
    """Test that the python script bootstrap.py was generated."""
    py_path = '/home/user/bootstrap.py'
    assert os.path.exists(py_path), f"The script {py_path} was not created."
    assert os.path.isfile(py_path), f"{py_path} is not a file."

def test_final_ci_matches_expected():
    """Test that final_ci.txt contains the correctly computed confidence interval."""
    final_ci_path = '/home/user/final_ci.txt'
    expected_ci_path = '/home/user/expected_final_ci.txt'

    assert os.path.exists(final_ci_path), f"The output file {final_ci_path} was not created."
    assert os.path.exists(expected_ci_path), "The expected truth file is missing (setup issue)."

    with open(final_ci_path, 'r') as f:
        actual_ci = f.read().strip()

    with open(expected_ci_path, 'r') as f:
        expected_ci = f.read().strip()

    assert actual_ci == expected_ci, f"Expected CI output '{expected_ci}', but got '{actual_ci}'."