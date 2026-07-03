# test_final_state.py
import os
import subprocess
import pytest
import json

MINIMAL_CRASH_PATH = "/home/user/minimal_crash.ndjson"
PROCESSOR_PATH = "/home/user/processor.py"
FIXED_PROCESSOR_PATH = "/home/user/fixed_processor.py"
SENSOR_LOGS_PATH = "/home/user/sensor_logs.ndjson"

def test_minimal_crash_exists_and_length():
    """Check if minimal_crash.ndjson exists and contains exactly 5 lines."""
    assert os.path.isfile(MINIMAL_CRASH_PATH), f"Expected file {MINIMAL_CRASH_PATH} to exist."

    with open(MINIMAL_CRASH_PATH, 'r') as f:
        lines = [line for line in f.read().splitlines() if line.strip()]

    assert len(lines) == 5, f"Expected {MINIMAL_CRASH_PATH} to contain exactly 5 lines, found {len(lines)}."

    # Verify they are valid JSON
    for line in lines:
        try:
            json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line in {MINIMAL_CRASH_PATH} is not valid JSON: {line}")

def test_minimal_crash_reproduces_bug():
    """Check if running the original processor against minimal_crash.ndjson crashes."""
    assert os.path.isfile(PROCESSOR_PATH), f"Expected {PROCESSOR_PATH} to exist."

    result = subprocess.run(
        ["python3", PROCESSOR_PATH, MINIMAL_CRASH_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0, f"Expected {PROCESSOR_PATH} to crash (non-zero exit code) on {MINIMAL_CRASH_PATH}."

def test_fixed_processor_exists_and_works():
    """Check if fixed_processor.py exists and successfully processes sensor_logs.ndjson."""
    assert os.path.isfile(FIXED_PROCESSOR_PATH), f"Expected file {FIXED_PROCESSOR_PATH} to exist."
    assert os.path.isfile(SENSOR_LOGS_PATH), f"Expected file {SENSOR_LOGS_PATH} to exist."

    result = subprocess.run(
        ["python3", FIXED_PROCESSOR_PATH, SENSOR_LOGS_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Expected {FIXED_PROCESSOR_PATH} to succeed (exit code 0), got {result.returncode}. Stderr: {result.stderr}"
    assert "Success" in result.stdout, f"Expected 'Success' in stdout, got: {result.stdout}"

def test_fixed_processor_logic():
    """Check if fixed_processor.py handles the ValueError and defaults to -1."""
    with open(FIXED_PROCESSOR_PATH, 'r') as f:
        content = f.read()

    # We expect a try/except block around the int() conversion or similar logic
    # The requirement is: defaulting the problematic field to -1 when it cannot be parsed as an integer
    assert "-1" in content, "Expected fixed_processor.py to contain the fallback value '-1'."