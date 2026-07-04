# test_final_state.py

import os
import re

def test_fit_model_c_modified():
    file_path = "/home/user/fit_model.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    # Check that double is used for total_prob
    assert re.search(r"double\s+total_prob\s*=\s*0\.0;", content), "The accumulator 'total_prob' was not changed to 'double'."

    # Check that double is used for p_vals
    assert re.search(r"double\s*\*\s*p_vals\s*=\s*malloc\(N\s*\*\s*sizeof\(double\)\);", content), "The array 'p_vals' was not changed to 'double'."

    # Ensure float is no longer used for these variables
    assert "float total_prob" not in content, "'float total_prob' is still present in the file."
    assert "float* p_vals" not in content, "'float* p_vals' is still present in the file."

def test_executable_exists():
    exe_path = "/home/user/fit_model"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did you compile the C program?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_results_txt_content():
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {results_path}, but found {len(lines)}."

    assert lines[0] == "0.00000000", f"Expected first line to be '0.00000000', got '{lines[0]}'."
    assert lines[1] == "0.00000000", f"Expected second line to be '0.00000000', got '{lines[1]}'."