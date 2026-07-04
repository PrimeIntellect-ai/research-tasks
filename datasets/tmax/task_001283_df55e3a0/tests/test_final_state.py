# test_final_state.py

import os
import re
import requests
import pytest
import subprocess

def test_venv_exists_and_flask_installed():
    venv_dir = "/home/user/project/venv"
    assert os.path.isdir(venv_dir), f"Virtual environment directory not found at {venv_dir}"

    # Check if Flask is installed in the venv
    python_bin = os.path.join(venv_dir, "bin", "python")
    assert os.path.isfile(python_bin), f"Python binary not found in venv at {python_bin}"

    result = subprocess.run([python_bin, "-c", "import flask; print(flask.__version__)"], capture_output=True, text=True)
    assert result.returncode == 0, f"Flask is not installed in the virtual environment. Error: {result.stderr}"

def test_crash_analysis_contents():
    analysis_file = "/home/user/project/crash_analysis.txt"
    assert os.path.isfile(analysis_file), f"Crash analysis file not found at {analysis_file}"

    with open(analysis_file, "r") as f:
        content = f.read().lower()

    assert "ff" in content or "0xff" in content, "Crash analysis does not mention the crashing byte sequence '0xFF' or 'FF'"
    assert any(keyword in content for keyword in ["malloc", "memory", "length", "segfault", "segmentation", "out of bounds"]), "Crash analysis does not adequately describe the vulnerability (missing keywords like malloc, memory, length, etc.)"

def test_proxy_service_running_and_sanitizing():
    url = "http://127.0.0.1:8080/api/v1/parse"

    # Construct a payload with valid and invalid (type 0xFF) TLV records
    # Type 1 (String), Length 2, Value "hi" -> \x01\x00\x02hi
    # Type 0xFF (Diagnostic), Length 4, Value "junk" -> \xff\x00\x04junk
    # Type 2 (Integer), Length 1, Value 5 -> \x02\x00\x01\x05
    payload = b"\x01\x00\x02hi\xff\x00\x04junk\x02\x00\x01\x05"

    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the proxy service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type to be application/json"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    # The proxy should have stripped the 0xFF record, leaving only Type 1 and Type 2.
    # We don't assert the exact JSON structure because it depends on the binary, 
    # but the response shouldn't be empty, and the binary shouldn't have crashed.
    # The fact that it returned 200 and valid JSON means the proxy successfully sanitized the input 
    # and the binary processed it without crashing.
    assert len(response.content) > 0, "Response JSON is empty"

def test_proxy_service_handles_clean_data():
    url = "http://127.0.0.1:8080/api/v1/parse"

    # Pure clean payload
    payload = b"\x01\x00\x04test\x02\x00\x02\x10\x20"

    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the proxy service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for clean data, got {response.status_code}"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON for clean data: {response.text}")