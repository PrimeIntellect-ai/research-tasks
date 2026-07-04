# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

def test_cargo_test_passes():
    """Verify that cargo test passes cleanly in /app/math-daemon."""
    app_dir = "/app/math-daemon"
    assert os.path.isdir(app_dir), f"Directory {app_dir} does not exist."

    try:
        result = subprocess.run(
            ["cargo", "test"],
            cwd=app_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        assert result.returncode == 0, f"cargo test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("cargo test timed out after 60 seconds.")

def test_service_eval_valid():
    """Verify the service evaluates valid bytecode correctly."""
    url = "http://127.0.0.1:9000/eval"
    payload = {"bytecode": [1, 20, 1, 4, 4]}

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        assert data.get("result") == 5, f"Expected result 5, got {data.get('result')}"
        assert data.get("error") is None, f"Expected error to be null, got {data.get('error')}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service or bad response: {e}")

def test_service_eval_division_by_zero():
    """Verify the service handles division by zero gracefully."""
    url = "http://127.0.0.1:9000/eval"
    payload = {"bytecode": [1, 10, 1, 0, 4]}

    try:
        response = requests.post(url, json=payload, timeout=5)
        # The agent might return 200 or 400, so we just check the JSON payload.
        data = response.json()
        assert data.get("result") is None, f"Expected result to be null, got {data.get('result')}"
        assert data.get("error") == "DivisionByZero", f"Expected error 'DivisionByZero', got {data.get('error')}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service or bad response: {e}")