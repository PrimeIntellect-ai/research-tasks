# test_final_state.py

import os
import pytest

def test_evaluate_knn_c_exists():
    file_path = "/home/user/evaluate_knn.c"
    assert os.path.isfile(file_path), f"Missing required C source file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read()

    # Basic check to ensure it's a C file (contains standard includes or main)
    assert "main" in content or "#include" in content, f"{file_path} does not appear to be a valid C source file."

def test_best_model_txt_correct():
    file_path = "/home/user/best_model.txt"
    assert os.path.isfile(file_path), f"Missing required output file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_output = "Best k: 7, Accuracy: 84.00%"
    assert content == expected_output, f"Incorrect content in {file_path}. Expected '{expected_output}', but got '{content}'"