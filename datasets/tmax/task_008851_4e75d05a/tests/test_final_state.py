# test_final_state.py

import os
import pytest

def test_c_source_code_exists():
    source_path = "/home/user/etl_infer.c"
    assert os.path.isfile(source_path), f"The C source code file {source_path} does not exist."

def test_executable_exists():
    executable_path = "/home/user/etl_infer"
    assert os.path.isfile(executable_path), f"The executable file {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_best_model_output():
    output_path = "/home/user/best_model.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected = "Model: 2, MSE: 1.3225"
    assert content == expected, f"The content of {output_path} is incorrect. Expected '{expected}', got '{content}'."