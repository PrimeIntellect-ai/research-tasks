# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/artifact_validator"
HIDDEN_TESTS_DIR = "/home/user/hidden_tests"

def test_binary_exists_and_executable():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary {BINARY_PATH} is missing."
    assert os.access(BINARY_PATH, os.X_OK), f"Compiled binary {BINARY_PATH} is not executable."

def run_validator(req_file):
    req_path = os.path.join(HIDDEN_TESTS_DIR, req_file)
    assert os.path.isfile(req_path), f"Test file {req_path} is missing."

    result = subprocess.run(
        [BINARY_PATH, req_path],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def test_valid_request():
    output = run_validator("req1.txt")
    expected = "VALID /artifacts/release/v2.1.0/bin.tar.gz"
    assert output == expected, f"Expected '{expected}', but got '{output}' for req1.txt"

def test_traversal_rejection():
    output = run_validator("req2.txt")
    expected = "REJECTED TRAVERSAL"
    assert output == expected, f"Expected '{expected}', but got '{output}' for req2.txt"

def test_invalid_route_rejection():
    output = run_validator("req3.txt")
    expected = "REJECTED INVALID_ROUTE"
    assert output == expected, f"Expected '{expected}', but got '{output}' for req3.txt"

def test_bad_token_short():
    output = run_validator("req4.txt")
    expected = "REJECTED BAD_TOKEN"
    assert output == expected, f"Expected '{expected}', but got '{output}' for req4.txt"

def test_bad_token_missing():
    output = run_validator("req5.txt")
    expected = "REJECTED BAD_TOKEN"
    assert output == expected, f"Expected '{expected}', but got '{output}' for req5.txt"