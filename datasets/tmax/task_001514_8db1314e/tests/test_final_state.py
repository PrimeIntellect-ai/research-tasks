# test_final_state.py

import os
import re
import subprocess
import pytest

def get_expected_payload():
    dump_path = "/home/user/memory.dump"
    assert os.path.isfile(dump_path), f"File not found: {dump_path}"

    with open(dump_path, 'rb') as f:
        content = f.read()

    # Extract the payload starting with CRASH_PAYLOAD:
    match = re.search(b'(CRASH_PAYLOAD:[A-Za-z0-9_]+)', content)
    assert match is not None, "Could not find CRASH_PAYLOAD in memory.dump"
    return match.group(1).decode('utf-8')

def test_bad_payload_file():
    payload_path = "/home/user/bad_payload.txt"
    assert os.path.isfile(payload_path), f"File not found: {payload_path}"

    with open(payload_path, 'r') as f:
        content = f.read().strip()

    expected_payload = get_expected_payload()
    assert content == expected_payload, f"Contents of {payload_path} do not match the expected payload."

def test_service_fixed_executable():
    executable_path = "/home/user/service_fixed"
    assert os.path.isfile(executable_path), f"Executable not found: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_service_fixed_execution():
    executable_path = "/home/user/service_fixed"
    payload_path = "/home/user/bad_payload.txt"

    assert os.path.isfile(executable_path), f"Executable not found: {executable_path}"
    assert os.path.isfile(payload_path), f"Payload file not found: {payload_path}"

    with open(payload_path, 'r') as f:
        payload_data = f.read()

    try:
        result = subprocess.run(
            [executable_path],
            input=payload_data,
            text=True,
            timeout=2.0,
            capture_output=True
        )
        assert result.returncode == 0, f"service_fixed crashed or returned non-zero exit code: {result.returncode}. Stderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("service_fixed timed out (infinite recursion not fixed).")