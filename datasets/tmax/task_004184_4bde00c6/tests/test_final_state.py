# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
MINIMAL_CRASH_PATH = os.path.join(WORKSPACE_DIR, "minimal_crash.txt")
BEACON_PARSER_PATH = os.path.join(WORKSPACE_DIR, "beacon_parser.py")
TEST_PARSER_PATH = os.path.join(WORKSPACE_DIR, "test_parser.py")

def test_minimal_crash_exists():
    assert os.path.isfile(MINIMAL_CRASH_PATH), f"The file {MINIMAL_CRASH_PATH} is missing. Delta debugging was not saved correctly."
    with open(MINIMAL_CRASH_PATH, 'r') as f:
        content = f.read().strip()
    assert len(content) > 0, f"The file {MINIMAL_CRASH_PATH} is empty."

def test_beacon_parser_fixed():
    assert os.path.isfile(BEACON_PARSER_PATH), f"The file {BEACON_PARSER_PATH} is missing."

    # Test payload that previously failed due to float precision and trailing comma
    test_payload = "0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,PAD,"
    cmd = ["python3", BEACON_PARSER_PATH, "--payload", test_payload]

    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, (
        f"beacon_parser.py failed to process the payload '{test_payload}'.\n"
        f"Standard Error: {result.stderr}\n"
        "Ensure both the floating-point precision bug and the empty segment/trailing comma bug are fixed."
    )

def test_regression_test_suite_passes():
    assert os.path.isfile(TEST_PARSER_PATH), f"The regression test file {TEST_PARSER_PATH} is missing."

    # Try running with pytest first
    result = subprocess.run(["python3", "-m", "pytest", TEST_PARSER_PATH], capture_output=True, text=True)

    if result.returncode != 0:
        # Fallback to running directly if it's a unittest script
        result = subprocess.run(["python3", TEST_PARSER_PATH], capture_output=True, text=True)

    assert result.returncode == 0, (
        f"The regression test suite {TEST_PARSER_PATH} failed to execute successfully.\n"
        f"Output:\n{result.stdout}\n{result.stderr}"
    )