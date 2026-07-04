# test_final_state.py

import os
import json
import pytest
import requests

def test_extractor_binary_exists_and_executable():
    binary_path = "/app/bin/extractor"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist"
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable"

def test_config_json_content():
    config_path = "/app/config/pipeline.json"
    assert os.path.isfile(config_path), f"{config_path} does not exist"
    with open(config_path, "r") as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {config_path} as JSON")

    expected = {"max_duration_seconds": 300, "require_stego": True, "strict_mode": 1}
    assert config_data == expected, f"{config_path} content does not match expected structure"

def test_benchmark_results():
    results_path = "/app/benchmark_results.json"
    assert os.path.isfile(results_path), f"{results_path} does not exist"
    with open(results_path, "r") as f:
        try:
            results_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {results_path} as JSON")

    assert "average_latency_ms" in results_data, f"'average_latency_ms' key missing in {results_path}"
    assert isinstance(results_data["average_latency_ms"], (int, float)), "'average_latency_ms' must be a number"

def test_api_analyze_endpoint():
    url = "http://127.0.0.1:8080/analyze"
    try:
        response = requests.post(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = {
        "status": "success",
        "duration": 12,
        "transcript": "PIPELINE_OK_992"
    }

    assert data == expected_data, f"API response JSON {data} does not match expected {expected_data}"