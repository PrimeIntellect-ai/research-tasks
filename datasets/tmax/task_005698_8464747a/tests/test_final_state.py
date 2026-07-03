# test_final_state.py

import os
import json
import pytest
import math

WORKSPACE_DIR = "/home/user/workspace"
LIB_PATH = os.path.join(WORKSPACE_DIR, "libmath.so")
TEST_SCRIPT_PATH = os.path.join(WORKSPACE_DIR, "test_integration.py")
OUTPUT_JSON_PATH = os.path.join(WORKSPACE_DIR, "integration_output.json")
SERVER_SCRIPT_PATH = os.path.join(WORKSPACE_DIR, "server.py")

def test_shared_library_compiled():
    assert os.path.exists(LIB_PATH), f"Shared library {LIB_PATH} was not compiled."
    assert os.path.isfile(LIB_PATH), f"{LIB_PATH} is not a file."

def test_integration_script_exists():
    assert os.path.exists(TEST_SCRIPT_PATH), f"Integration test script {TEST_SCRIPT_PATH} is missing."
    assert os.path.isfile(TEST_SCRIPT_PATH), f"{TEST_SCRIPT_PATH} is not a file."

def test_server_script_modified():
    assert os.path.exists(SERVER_SCRIPT_PATH), f"Server script {SERVER_SCRIPT_PATH} is missing."
    with open(SERVER_SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "argtypes" in content, "server.py does not seem to configure 'argtypes' for the C function."
    assert "restype" in content, "server.py does not seem to configure 'restype' for the C function."

def test_integration_output_correct():
    assert os.path.exists(OUTPUT_JSON_PATH), f"Output JSON file {OUTPUT_JSON_PATH} is missing. Did you run the integration test?"

    with open(OUTPUT_JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{OUTPUT_JSON_PATH} does not contain valid JSON.")

    assert "result" in data, f"'result' key missing in {OUTPUT_JSON_PATH}."

    # The variance of [10.5, 15.2, 12.8, 9.1, 14.4] is exactly 5.3
    expected_variance = 5.3
    actual_variance = data["result"]

    assert isinstance(actual_variance, (int, float)), f"Result should be a number, got {type(actual_variance)}"
    assert math.isclose(actual_variance, expected_variance, rel_tol=1e-4), \
        f"Expected variance approximately {expected_variance}, got {actual_variance}."