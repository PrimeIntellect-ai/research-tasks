# test_final_state.py

import os
import pytest

DATA_DIR = "/home/user/data"
SCRIPT_PATH = "/home/user/process_etl.sh"
TRAIN_FINAL_PATH = os.path.join(DATA_DIR, "train_final.csv")
TEST_FINAL_PATH = os.path.join(DATA_DIR, "test_final.csv")

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_train_final_content():
    assert os.path.isfile(TRAIN_FINAL_PATH), f"Output file {TRAIN_FINAL_PATH} was not created."

    with open(TRAIN_FINAL_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "id,scaled_adjusted_reading",
        "1,0.0000",
        "2,1.0000",
        "3,0.2000",
        "4,0.0000"
    ]

    assert lines == expected_lines, f"Content of {TRAIN_FINAL_PATH} is incorrect. Expected {expected_lines}, got {lines}."

def test_test_final_content():
    assert os.path.isfile(TEST_FINAL_PATH), f"Output file {TEST_FINAL_PATH} was not created."

    with open(TEST_FINAL_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "id,scaled_adjusted_reading",
        "5,1.0000",
        "6,1.4000",
        "7,0.6000"
    ]

    assert lines == expected_lines, f"Content of {TEST_FINAL_PATH} is incorrect. Expected {expected_lines}, got {lines}."