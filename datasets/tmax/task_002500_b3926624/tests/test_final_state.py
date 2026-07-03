# test_final_state.py
import os
import subprocess
import requests
import time

def test_model_script_exists_and_executable():
    """Verify that the model.sh script exists and is executable."""
    script_path = "/home/user/model.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_test_model_script_exists_and_passes():
    """Verify that the test_model.sh script exists and exits with 0."""
    script_path = "/home/user/test_model.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"test_model.sh failed with exit code {result.returncode}:\n{result.stderr}"

def test_http_server_result():
    """Verify that the HTTP server responds correctly to GET /result."""
    url = "http://127.0.0.1:8080/result"

    # Retry a few times in case the server is slow to respond
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            break
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                assert False, f"Failed to connect to the HTTP server at {url}: {e}"
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response body is not valid JSON: {response.text}"

    assert "k1" in data, "JSON response missing 'k1' key"
    assert "k2" in data, "JSON response missing 'k2' key"

    assert data["k1"] == 50, f"Expected k1=50, got {data['k1']}"
    assert float(data["k2"]) == 0.5, f"Expected k2=0.5, got {data['k2']}"