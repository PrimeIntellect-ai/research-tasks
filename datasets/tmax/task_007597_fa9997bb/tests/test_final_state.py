# test_final_state.py

import os
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_train_processed_output():
    train_path = "/home/user/train_processed.csv"
    assert os.path.exists(train_path), f"Output file {train_path} does not exist."
    assert os.path.isfile(train_path), f"Path {train_path} is not a file."

    expected_train = [
        "1|hello world|0|22",
        "2|bash is great for text processing|1|22",
        "3|data science in the shell|1|22",
        "5|another valid row|0|22",
        "6|short text|1|22",
        "7|a very very long text string for testing|0|22"
    ]

    with open(train_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_train, f"Content of {train_path} does not match expected output. Got: {lines}"

def test_test_processed_output():
    test_path = "/home/user/test_processed.csv"
    assert os.path.exists(test_path), f"Output file {test_path} does not exist."
    assert os.path.isfile(test_path), f"Path {test_path} is not a file."

    expected_test = [
        "8|testing dataset|1|22",
        "9|more data|0|22",
        "10|final row|1|22"
    ]

    with open(test_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_test, f"Content of {test_path} does not match expected output. Got: {lines}"