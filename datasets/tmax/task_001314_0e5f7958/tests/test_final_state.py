# test_final_state.py

import os
import re

def test_result_txt_exists_and_correct():
    result_file = "/home/user/result.txt"
    assert os.path.isfile(result_file), f"File {result_file} is missing. Did you save the output?"

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert "Sum: 1000000.00000" in content, f"Expected 'Sum: 1000000.00000' in {result_file}, found:\n{content}"
    assert "Variance: 0.00000" in content, f"Expected 'Variance: 0.00000' in {result_file}, found:\n{content}"

def test_processor_executable_exists():
    executable_path = "/home/user/processor"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing. Did you compile the code?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_processor_c_fixed():
    file_path = "/home/user/processor.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    # Check that double is used for accumulation
    assert "double" in content, "The code does not seem to use 'double' precision as required."

    # Ensure the out-of-bounds bug is removed
    assert "end = num_elements + 1000;" not in content, "The out-of-bounds bug is still present in the code."