# test_final_state.py

import os
import urllib.request
import json
import subprocess
import pytest

def test_libmetric_so_exists():
    """Check if the shared library exists."""
    lib_path = "/home/user/metrics/libmetric.so"
    assert os.path.isfile(lib_path), f"Shared library not found at {lib_path}"

def test_integration_script_exists_and_executable():
    """Check if the integration test script exists and is executable."""
    script_path = "/home/user/metrics/test_integration.sh"
    assert os.path.isfile(script_path), f"Integration test script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Integration test script at {script_path} is not executable"

def test_web_service_stdev():
    """Test the web service for correct standard deviation calculation."""
    url = "http://127.0.0.1:8181/stdev?build_times=10,12,23,23,16,23,21,16"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = response.read().decode('utf-8')
            try:
                json_data = json.loads(data)
            except json.JSONDecodeError:
                pytest.fail(f"Response is not valid JSON: {data}")

            assert "stdev" in json_data, "Response JSON does not contain 'stdev' key"
            # The stdev of [10, 12, 23, 23, 16, 23, 21, 16] is approx 5.244
            assert json_data["stdev"] == 5.24, f"Expected stdev to be 5.24, got {json_data['stdev']}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the web service at {url}: {e}")

def test_run_user_integration_script():
    """Run the user's integration test script and ensure it succeeds."""
    script_path = "/home/user/metrics/test_integration.sh"
    try:
        result = subprocess.run([script_path], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"Integration script failed with exit code {result.returncode}. Output:\n{result.stdout}\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Integration script timed out after 10 seconds.")
    except Exception as e:
        pytest.fail(f"Failed to execute integration script: {e}")