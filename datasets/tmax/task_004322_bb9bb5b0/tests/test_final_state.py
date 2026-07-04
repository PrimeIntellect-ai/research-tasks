# test_final_state.py

import os
import json
import zlib
import subprocess
import pytest

def test_venv_exists():
    """Test that the virtual environment was created."""
    python_path = '/home/user/venv/bin/python'
    assert os.path.exists(python_path), f"Virtual environment Python executable not found at {python_path}."

def test_websockets_installed():
    """Test that the websockets package is installed in the virtual environment."""
    python_path = '/home/user/venv/bin/python'
    if not os.path.exists(python_path):
        pytest.fail("Virtual environment not found, cannot check for websockets.")

    result = subprocess.run([python_path, '-c', 'import websockets'], capture_output=True)
    assert result.returncode == 0, "The 'websockets' package is not installed in the virtual environment."

def test_success_log_content():
    """Test that success.log exists and contains the correct payload and checksum."""
    log_path = '/home/user/success.log'
    data_path = '/home/user/data.json'

    assert os.path.exists(log_path), f"{log_path} is missing. The script may not have run successfully."
    assert os.path.exists(data_path), f"{data_path} is missing."

    # Compute expected values based on data.json
    with open(data_path, 'r') as f:
        data = json.load(f)

    expected_payload = json.dumps(data, sort_keys=True)
    expected_checksum = zlib.crc32(expected_payload.encode('utf-8'))

    # Read actual output
    with open(log_path, 'r') as f:
        log_content = f.read()

    try:
        log_data = json.loads(log_content)
    except json.JSONDecodeError:
        pytest.fail(f"{log_path} does not contain valid JSON.")

    assert "payload" in log_data, f"'payload' key missing in {log_path}."
    assert "checksum" in log_data, f"'checksum' key missing in {log_path}."

    assert log_data["payload"] == expected_payload, f"Expected payload '{expected_payload}', but got '{log_data['payload']}'."
    assert log_data["checksum"] == expected_checksum, f"Expected checksum {expected_checksum}, but got {log_data['checksum']}."