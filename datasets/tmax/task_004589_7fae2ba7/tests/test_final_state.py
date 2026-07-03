# test_final_state.py
import os
import json
import math
import subprocess
import requests
import pytest

def test_pipeline_executable_and_idempotent():
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"{pipeline_path} does not exist."
    assert os.access(pipeline_path, os.X_OK), f"{pipeline_path} is not executable."

    # Execute pipeline twice to test idempotency
    try:
        subprocess.run([pipeline_path], check=True, timeout=30)
        subprocess.run([pipeline_path], check=True, timeout=30)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Pipeline script failed to execute successfully: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail("Pipeline script execution timed out.")

    metrics_path = "/home/user/metrics.csv"
    assert os.path.isfile(metrics_path), f"{metrics_path} was not created."

    with open(metrics_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 10, f"Expected exactly 10 records in {metrics_path} after two runs (idempotency check), but found {len(lines)}."

def test_summary_json_contents():
    summary_path = "/home/user/summary.json"
    assert os.path.isfile(summary_path), f"{summary_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{summary_path} does not contain valid JSON.")

    assert "average_volume" in data, "Missing 'average_volume' in summary.json."
    assert "euclidean_distance" in data, "Missing 'euclidean_distance' in summary.json."
    assert "record_count" in data, "Missing 'record_count' in summary.json."

    assert int(data["record_count"]) == 10, f"Expected record_count to be 10, got {data['record_count']}."

    avg_vol = float(data["average_volume"])
    euc_dist = float(data["euclidean_distance"])

    assert math.isclose(avg_vol, 77.78, abs_tol=2.0), f"average_volume {avg_vol} is not close to expected ~77.8."
    assert math.isclose(euc_dist, 201.2, abs_tol=5.0), f"euclidean_distance {euc_dist} is not close to expected ~201.2."

def test_http_server_response():
    server_path = "/home/user/server.sh"
    assert os.path.isfile(server_path), f"{server_path} does not exist."
    assert os.access(server_path, os.X_OK), f"{server_path} is not executable."

    try:
        response = requests.get("http://127.0.0.1:8080/api/v1/metrics", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server on port 8080 or request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type to contain application/json, got {content_type}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"API response body is not valid JSON. Response text: {response.text}")

    assert "average_volume" in data, "Missing 'average_volume' in API JSON response."
    assert "euclidean_distance" in data, "Missing 'euclidean_distance' in API JSON response."
    assert "record_count" in data, "Missing 'record_count' in API JSON response."