# test_final_state.py

import os
import time
import subprocess
import requests
import pytest

SCRIPT_PATH = "/home/user/start_server.sh"
URL = "http://127.0.0.1:8080/features"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_server_response():
    # Attempt to start the server
    process = subprocess.Popen([SCRIPT_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for the server to start
    max_retries = 10
    server_up = False
    for _ in range(max_retries):
        try:
            response = requests.get(URL, timeout=1)
            if response.status_code == 200:
                server_up = True
                break
        except requests.exceptions.RequestException:
            time.sleep(0.5)

    try:
        assert server_up, f"Failed to connect to the server at {URL} after starting {SCRIPT_PATH}."

        # Check Content-Type
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type.lower(), f"Expected Content-Type: application/json, got {content_type}"

        # Check JSON response
        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response body is not valid JSON. Got: {response.text}")

        assert "peak_frequency_hz" in data, "JSON response missing 'peak_frequency_hz' key."
        assert "atom_count" in data, "JSON response missing 'atom_count' key."

        assert data["peak_frequency_hz"] == 850, f"Expected peak_frequency_hz to be 850, got {data['peak_frequency_hz']}"
        assert data["atom_count"] == 42, f"Expected atom_count to be 42, got {data['atom_count']}"

    finally:
        # Cleanup the server process
        process.terminate()
        process.wait(timeout=2)