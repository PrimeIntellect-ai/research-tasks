# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/app/handler.sh"
DB_PATH = "/home/user/app/packages.db"

def run_handler(input_string: str) -> str:
    """Helper to run the handler script with the given input string on stdin."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

    result = subprocess.run(
        [SCRIPT_PATH],
        input=input_string,
        text=True,
        capture_output=True,
        timeout=5 # Prevent infinite loops from hanging the tests completely
    )
    return result.stdout.strip()

def test_handler_successful_resolution():
    """Test that the handler correctly resolves a complex dependency graph and formats the output."""
    input_str = "RESOLVE /api/deps?foo=bar&pkg=web_server&baz=1"
    try:
        output = run_handler(input_str)
    except subprocess.TimeoutExpired:
        pytest.fail("The script timed out, likely due to an infinite loop.")

    expected = "SUCCESS: config disk filesystem http logger network system tcp"
    assert output == expected, f"Expected output '{expected}', but got '{output}'"

def test_handler_cycle_detection():
    """Test that the handler detects circular dependencies and halts with the correct error message."""
    input_str = "RESOLVE /api/deps?pkg=auth"
    try:
        output = run_handler(input_str)
    except subprocess.TimeoutExpired:
        pytest.fail("The script timed out on a circular dependency instead of detecting it.")

    expected = "ERROR: cycle detected"
    assert output == expected, f"Expected output '{expected}', but got '{output}'"

def test_handler_parameter_parsing_edge_cases():
    """Test that the handler correctly extracts the pkg parameter from various positions."""
    # pkg at the end
    out1 = run_handler("RESOLVE /api/deps?verbose=1&pkg=tcp")
    assert out1 == "SUCCESS: filesystem logger network system", f"Failed on pkg at end. Got: {out1}"

    # pkg at the beginning
    out2 = run_handler("RESOLVE /api/deps?pkg=tcp&verbose=1")
    assert out2 == "SUCCESS: filesystem logger network system", f"Failed on pkg at beginning. Got: {out2}"

    # pkg as the only parameter
    out3 = run_handler("RESOLVE /api/deps?pkg=tcp")
    assert out3 == "SUCCESS: filesystem logger network system", f"Failed on pkg as only parameter. Got: {out3}"