# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_release_bin_exists_and_statically_linked():
    """Check that the compiled binary exists at the correct path and is statically linked."""
    bin_path = "/home/user/release_bin"
    assert os.path.isfile(bin_path), f"Compiled binary is missing at {bin_path}"

    # Check if it's statically linked using the `file` command
    result = subprocess.run(["file", bin_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run file command on {bin_path}"
    assert "statically linked" in result.stdout, f"Binary at {bin_path} is not statically linked. File output: {result.stdout}"

def test_http_server_analyze_endpoint():
    """Check that the HTTP server is running and the /analyze endpoint works correctly."""
    url = "http://127.0.0.1:9000/analyze"

    try:
        response = requests.get(url, timeout=30)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Response: {response.text}")

    assert "secret" in data, f"JSON response missing 'secret' key. Response: {data}"

    secret_text = data["secret"].lower()

    # Check for the expected tokens
    expected_tokens = ["delta", "tango", "seven"]
    for token in expected_tokens:
        assert token in secret_text, f"Transcribed text is missing expected token '{token}'. Transcribed text: {data['secret']}"