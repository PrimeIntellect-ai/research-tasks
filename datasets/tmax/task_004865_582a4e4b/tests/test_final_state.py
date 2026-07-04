# test_final_state.py

import os
import subprocess
import pytest

def test_recovered_payload():
    """Verify the recovered payload exists and has the correct size."""
    payload_path = '/home/user/recovered_payload.dat'
    assert os.path.exists(payload_path), f"{payload_path} does not exist."

    size = os.path.getsize(payload_path)
    assert size == 256, f"Expected {payload_path} to be exactly 256 bytes, but got {size} bytes."

    with open(payload_path, 'rb') as f:
        data = f.read()
    assert b'\xFF' in data, f"Expected {payload_path} to contain 0xFF bytes."

def test_fix_verified_log():
    """Verify that fix_verified.log exists and contains the correct success message."""
    log_path = '/home/user/fix_verified.log'
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    expected_message = "Parse complete: 256 bytes"
    assert expected_message in content, f"Expected '{expected_message}' in {log_path}, got: {content}"

def test_fuzzer_success():
    """Verify that the fuzzer runs successfully without hanging."""
    fuzzer_path = '/home/user/fuzzer.py'
    assert os.path.exists(fuzzer_path), f"{fuzzer_path} does not exist."

    try:
        result = subprocess.run(
            ['python3', fuzzer_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            text=True,
            check=True
        )
        assert "Fuzzing complete. No hangs detected." in result.stdout, "Fuzzer did not output the expected success message."
    except subprocess.TimeoutExpired:
        pytest.fail("Fuzzer timed out, indicating the memory leak/hang is not fixed.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Fuzzer failed with exit code {e.returncode}. Output: {e.stdout} {e.stderr}")

def test_service_no_hang_on_recovered_payload():
    """Verify that the service can process the recovered payload without hanging."""
    service_path = '/home/user/service.py'
    payload_path = '/home/user/recovered_payload.dat'

    try:
        result = subprocess.run(
            ['python3', service_path, payload_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True,
            check=True
        )
        assert "Parse complete: 256 bytes" in result.stdout, "Service did not output the expected success message."
    except subprocess.TimeoutExpired:
        pytest.fail("Service timed out on the recovered payload, indicating the bug is not fixed.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Service failed on the recovered payload. Output: {e.stdout} {e.stderr}")