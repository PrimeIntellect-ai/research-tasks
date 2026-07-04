# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/project"
CONFIG_FILE = os.path.join(PROJECT_DIR, "config.b64")
BUILD_OUTPUT = os.path.join(PROJECT_DIR, "build_output.txt")

def test_config_file_recovered():
    assert os.path.exists(CONFIG_FILE), f"Recovered config file {CONFIG_FILE} is missing."
    assert os.path.isfile(CONFIG_FILE), f"{CONFIG_FILE} is not a file."

    with open(CONFIG_FILE, "r") as f:
        content = f.read().strip()

    expected_content = "MTUgMjUgMzUgNDUgNTU="
    assert content == expected_content, f"Content of {CONFIG_FILE} is incorrect. Expected '{expected_content}', got '{content}'."

def test_build_output_correct():
    assert os.path.exists(BUILD_OUTPUT), f"Build output file {BUILD_OUTPUT} is missing."
    assert os.path.isfile(BUILD_OUTPUT), f"{BUILD_OUTPUT} is not a file."

    with open(BUILD_OUTPUT, "r") as f:
        content = f.read().strip()

    expected_score = "625"
    assert content == expected_score, f"Build output is incorrect. Expected '{expected_score}', got '{content}'."