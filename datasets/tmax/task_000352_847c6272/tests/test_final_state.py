# test_final_state.py
import os
import json
import time
import subprocess
import urllib.request
import pytest

def test_files_exist():
    """Verify that all required files exist."""
    expected_files = [
        "/home/user/api.py",
        "/home/user/benchmark.sh",
        "/home/user/analyze.py",
        "/home/user/results.json"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"File {f} is missing."

def test_benchmark_executable():
    """Verify that the benchmark script is executable."""
    assert os.access("/home/user/benchmark.sh", os.X_OK), "/home/user/benchmark.sh is not executable."

def test_results_json_schema():
    """Verify that the results.json file has the correct schema and types."""
    with open("/home/user/results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/results.json is not valid JSON.")

    expected_keys = {"mean_1", "mean_4", "p_value", "ci_lower", "ci_upper", "significant"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(data.keys())}"

    assert isinstance(data["mean_1"], (int, float)), "mean_1 must be a float"
    assert isinstance(data["mean_4"], (int, float)), "mean_4 must be a float"
    assert isinstance(data["p_value"], (int, float)), "p_value must be a float"
    assert isinstance(data["ci_lower"], (int, float)), "ci_lower must be a float"
    assert isinstance(data["ci_upper"], (int, float)), "ci_upper must be a float"
    assert isinstance(data["significant"], bool), "significant must be a boolean"

def test_api_logic():
    """Verify that the API correctly computes cosine similarity."""
    try:
        import numpy as np
    except ImportError:
        pytest.fail("numpy is not installed.")

    # Start the API in the background
    proc = subprocess.Popen(["python3", "/home/user/api.py"])
    time.sleep(3) # Wait for the server to start

    try:
        vectors = np.load("/home/user/vectors.npy")
        # Use an existing vector to guarantee it's the exact top match
        test_query = vectors[42].tolist()

        req = urllib.request.Request(
            "http://127.0.0.1:8000/search",
            data=json.dumps({"query": test_query}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"Expected HTTP 200, got {response.status}"
                data = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            pytest.fail(f"Failed to query API: {e}")

        assert "top_indices" in data, "API response is missing the 'top_indices' key."
        assert len(data["top_indices"]) == 5, f"Expected 5 top indices, got {len(data['top_indices'])}."
        assert data["top_indices"][0] == 42, f"Expected the first index to be 42, got {data['top_indices'][0]}."
    finally:
        proc.terminate()
        proc.wait(timeout=5)