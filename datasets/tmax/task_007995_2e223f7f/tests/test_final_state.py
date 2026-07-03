# test_final_state.py

import os
import pytest

def test_evaluate_c_exists():
    file_path = "/home/user/evaluate.c"
    assert os.path.isfile(file_path), f"The C source file {file_path} does not exist. Did you write the program?"

def test_best_model_log_exists_and_correct():
    log_path = "/home/user/best_model.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist. Did you run your compiled C program?"

    with open(log_path, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) == 2, f"Expected exactly 2 lines in {log_path}, found {len(content)} lines."

    expected_line_1 = "Best Alpha: 0.50"
    expected_line_2 = "Lowest MSE: 0.0150"

    assert content[0].strip() == expected_line_1, f"Expected first line to be '{expected_line_1}', but got '{content[0]}'."
    assert content[1].strip() == expected_line_2, f"Expected second line to be '{expected_line_2}', but got '{content[1]}'."