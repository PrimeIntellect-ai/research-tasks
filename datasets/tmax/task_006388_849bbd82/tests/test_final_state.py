# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/project"
RESULT_FILE = os.path.join(PROJECT_DIR, "result.txt")
MAKEFILE = os.path.join(PROJECT_DIR, "Makefile")
APP_BIN = os.path.join(PROJECT_DIR, "bin", "app")

def test_makefile_exists():
    assert os.path.isfile(MAKEFILE), "Makefile was not generated in /home/user/project/."

def test_app_binary_exists():
    assert os.path.isfile(APP_BIN), "The compiled executable /home/user/project/bin/app does not exist."
    assert os.access(APP_BIN, os.X_OK), "The compiled file /home/user/project/bin/app is not executable."

def test_result_txt_exists():
    assert os.path.isfile(RESULT_FILE), "The result file /home/user/project/result.txt does not exist."

def test_result_txt_content():
    expected_content = (
        "Running in ARM mode\n"
        "Result: 8\n"
        "String ops loaded.\n"
    )

    with open(RESULT_FILE, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), (
        f"The content of {RESULT_FILE} is incorrect.\n"
        f"Expected:\n{expected_content.strip()}\n\n"
        f"Got:\n{content.strip()}"
    )