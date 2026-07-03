# test_final_state.py

import os
import pytest

def test_executable_exists():
    executable_path = "/home/user/prepare_cv"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist. Did you compile the C code?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_results_file_contents():
    results_path = "/home/user/cv_results.txt"
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist. Did you run the executable and redirect output?"

    with open(results_path, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) == 3, f"Expected 3 lines in {results_path}, but found {len(content)}."

    expected_lines = [
        "Fold 1: train_threshold = 60.00, val_accuracy = 1.00",
        "Fold 2: train_threshold = 47.50, val_accuracy = 0.50",
        "Fold 3: train_threshold = 27.50, val_accuracy = 1.00"
    ]

    for i, expected in enumerate(expected_lines):
        assert content[i].strip() == expected, f"Line {i+1} in {results_path} is incorrect. Expected: '{expected}', Got: '{content[i].strip()}'"

def test_c_code_fixed():
    filepath = "/home/user/prepare_cv.c"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        content = f.read()

    # The exact string might have been removed or modified, but we can check that it's no longer just assigning the global threshold
    # A simple heuristic: check if `train_threshold = global_threshold;` is absent, or check that the logic has changed.
    assert "double train_threshold = global_threshold;" not in content, "The file still assigns the global threshold directly to train_threshold. Data leakage is not fixed."