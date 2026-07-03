# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import pytest

def test_processed_sensors_csv():
    """Verify that processed_sensors.csv exists and has the correct number of rows."""
    file_path = "/home/user/processed_sensors.csv"
    assert os.path.isfile(file_path), f"Processed dataset is missing: {file_path}"

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # 4960 data rows + 1 header row = 4961 lines
    assert len(lines) == 4961, f"Expected 4961 lines in {file_path}, but found {len(lines)}."

def test_best_params_json():
    """Verify that best_params.json exists and contains the required keys."""
    file_path = "/home/user/best_params.json"
    assert os.path.isfile(file_path), f"Best parameters file is missing: {file_path}"

    with open(file_path, 'r') as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert "max_depth" in params, "Key 'max_depth' is missing from best_params.json."
    assert "n_estimators" in params, "Key 'n_estimators' is missing from best_params.json."

def test_benchmark_status():
    """Verify that benchmark_status.txt exists and contains 'SUCCESS'."""
    file_path = "/home/user/benchmark_status.txt"
    assert os.path.isfile(file_path), f"Benchmark status file is missing: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "SUCCESS", f"Expected benchmark_status.txt to contain 'SUCCESS', but got '{content}'."

def test_api_predict():
    """Verify that the FastAPI /predict endpoint is running and returns the correct format."""
    url = "http://127.0.0.1:8000/predict"
    payload = {
        "temperature": 0.5,
        "vibration": 0.5,
        "pressure": 0.5
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            response_data = response.read().decode('utf-8')
            try:
                result = json.loads(response_data)
            except json.JSONDecodeError:
                pytest.fail("API response is not valid JSON.")

            assert "status" in result, "Response JSON is missing 'status' key."
            assert isinstance(result["status"], int), "The 'status' value in response must be an integer."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")