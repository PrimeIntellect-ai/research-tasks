# test_final_state.py

import os
import pytest

def test_evaluate_model_script_exists():
    path = "/home/user/evaluate_model.py"
    assert os.path.isfile(path), f"The script {path} is missing."

def test_test_pipeline_script_exists():
    path = "/home/user/test_pipeline.py"
    assert os.path.isfile(path), f"The script {path} is missing."

def test_accuracy_file_exists_and_content():
    path = "/home/user/accuracy.txt"
    assert os.path.isfile(path), f"The output file {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "1.0000", f"Expected accuracy.txt to contain '1.0000', but got '{content}'."

def test_test_pass_log_exists():
    path = "/home/user/test_pass.log"
    assert os.path.isfile(path), f"The log file {path} is missing. The reproducibility test may have failed or was not executed."