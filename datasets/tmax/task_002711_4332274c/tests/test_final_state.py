# test_final_state.py
import os
import requests
import pytest
import time

def test_files_exist():
    expected_files = [
        "/home/user/server.go",
        "/home/user/benchmark.sh",
        "/home/user/benchmark_results.txt"
    ]
    for path in expected_files:
        assert os.path.isfile(path), f"Expected file missing: {path}"

def test_server_running_and_search_endpoint():
    url = "http://127.0.0.1:8080/search"

    # Wait for the server to be up if it isn't already
    max_retries = 5
    for i in range(max_retries):
        try:
            # P001 description
            payload = {"query": "High quality wireless mouse", "k": 1}
            response = requests.post(url, json=payload, timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(1)
    else:
        pytest.fail("Server is not running or not responding on 127.0.0.1:8080")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Response should be a JSON array"
    assert len(data) == 1, "Expected exactly 1 result for k=1"

    top_result = data[0]
    assert "product_id" in top_result, "Result missing 'product_id'"
    assert "score" in top_result, "Result missing 'score'"

    # Since we query with exact description of P001, it should be the top result
    assert top_result["product_id"] == "P001", "Expected P001 as top result for its own description"

def test_search_endpoint_p004():
    url = "http://127.0.0.1:8080/search"
    payload = {"query": "Noise cancelling bluetooth headphones", "k": 2}

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Response should be a JSON array"
    assert len(data) <= 2, "Expected at most 2 results for k=2"
    assert len(data) > 0, "Expected at least 1 result"

    top_result = data[0]
    assert top_result["product_id"] == "P004", "Expected P004 as top result for its own description"

    # Ensure P002, P003, P005 are filtered out
    product_ids = [item["product_id"] for item in data]
    for invalid_id in ["P002", "P003", "P005"]:
        assert invalid_id not in product_ids, f"Cleaned dataset should not contain {invalid_id}"