# test_final_state.py

import os
import stat
import pytest

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"

    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_results_file_content():
    results_path = "/home/user/results.txt"

    assert os.path.exists(results_path), f"Results file {results_path} does not exist."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    expected_content = (
        "Control Mean: 149.00\n"
        "Treatment Mean: 203.63\n"
        "Absolute Difference: 54.63"
    )

    with open(results_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {results_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{actual_content}"
    )