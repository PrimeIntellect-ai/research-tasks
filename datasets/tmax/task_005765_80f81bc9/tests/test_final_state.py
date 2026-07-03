# test_final_state.py

import os

def test_telemetry_source_exists():
    path = "/home/user/telemetry.c"
    assert os.path.exists(path), f"Source file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

def test_telemetry_executable_exists():
    path = "/home/user/telemetry"
    assert os.path.exists(path), f"Executable {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_prop_test_exists_and_uses_hypothesis():
    path = "/home/user/prop_test.py"
    assert os.path.exists(path), f"Python test file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r") as f:
        content = f.read()

    assert "hypothesis" in content, f"File {path} does not contain 'hypothesis'."

def test_results_log_content():
    path = "/home/user/results.log"
    assert os.path.exists(path), f"Results log file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    expected_content = (
        "OK A1B2 100\n"
        "OK A1B2 200\n"
        "LIMIT A1B2\n"
        "LIMIT A1B2\n"
        "OK FFFF 5\n"
        "ERROR\n"
        "ERROR\n"
        "OK 1234 99999999\n"
    )

    with open(path, "r") as f:
        content = f.read()

    assert content == expected_content, f"Content of {path} does not match the expected output."