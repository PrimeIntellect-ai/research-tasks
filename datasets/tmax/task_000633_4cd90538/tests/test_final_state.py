# test_final_state.py

import os
import subprocess
import time
import requests
import pytest
import json

@pytest.fixture(scope="session", autouse=True)
def setup_and_run_services():
    # Run etl.sh
    etl_script = "/home/user/etl.sh"
    assert os.path.isfile(etl_script), f"Missing ETL script: {etl_script}"
    assert os.access(etl_script, os.X_OK), f"ETL script is not executable: {etl_script}"

    etl_process = subprocess.run([etl_script], capture_output=True, text=True)
    assert etl_process.returncode == 0, f"etl.sh failed with return code {etl_process.returncode}\nStdout: {etl_process.stdout}\nStderr: {etl_process.stderr}"

    # Run serve.sh
    serve_script = "/home/user/serve.sh"
    assert os.path.isfile(serve_script), f"Missing serve script: {serve_script}"
    assert os.access(serve_script, os.X_OK), f"Serve script is not executable: {serve_script}"

    serve_process = subprocess.Popen([serve_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the server to start
    time.sleep(2)

    yield

    # Teardown
    serve_process.terminate()
    serve_process.wait(timeout=5)

def test_final_dataset_exists_and_correct():
    dataset_path = "/home/user/processed/final_dataset.tsv"
    assert os.path.isfile(dataset_path), f"Missing final dataset: {dataset_path}"

    with open(dataset_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Check headers
    assert lines[0] == "event_id\tuser_id\tregion\tmetric_value\tsecure_token", "Incorrect headers in final_dataset.tsv"

    # Check data rows
    data_rows = lines[1:]
    assert len(data_rows) == 4, f"Expected 4 valid data rows, found {len(data_rows)}"

    # Expected rows:
    # 1001: 101, US-East, 50.5, TKN-3F2
    # 1004: 101, US-East, 100.0, TKN-3F5
    # 1005: 102, EU-West, 25.0, TKN-3F3
    # 1008: 103, US-East, 10.5, TKN-3E7

    expected_rows = {
        "1001\t101\tUS-East\t50.5\tTKN-3F2",
        "1004\t101\tUS-East\t100.0\tTKN-3F5",
        "1005\t102\tEU-West\t25.0\tTKN-3F3",
        "1008\t103\tUS-East\t10.5\tTKN-3E7"
    }

    actual_rows = set(data_rows)
    assert actual_rows == expected_rows, f"Data rows mismatch.\nExpected: {expected_rows}\nActual: {actual_rows}"

def test_etl_runs_log():
    log_path = "/home/user/etl_runs.log"
    assert os.path.isfile(log_path), f"Missing ETL runs log: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Processed 4 valid events" in content, f"Expected 'Processed 4 valid events' in {log_path}, got: {content}"

def test_serve_us_east_valid():
    url = "http://127.0.0.1:8080/query?region=US-East"
    headers = {"Authorization": "Bearer etl_secret_2024"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("region") == "US-East", f"Expected region US-East, got {data.get('region')}"
    assert float(data.get("total_metric", 0)) == 161.0, f"Expected total_metric 161.0, got {data.get('total_metric')}"

def test_serve_eu_west_valid():
    url = "http://127.0.0.1:8080/query?region=EU-West"
    headers = {"Authorization": "Bearer etl_secret_2024"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("region") == "EU-West", f"Expected region EU-West, got {data.get('region')}"
    assert float(data.get("total_metric", 0)) == 25.0, f"Expected total_metric 25.0, got {data.get('total_metric')}"

def test_serve_invalid_auth():
    url = "http://127.0.0.1:8080/query?region=US-East"

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_serve_missing_params():
    url = "http://127.0.0.1:8080/query"
    headers = {"Authorization": "Bearer etl_secret_2024"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code >= 400, f"Expected a 400+ error status code for missing params, got {response.status_code}. Response: {response.text}"