# test_final_state.py

import os
import re
import json
import math
import hashlib
import pytest
import requests

def deterministic_embedding(text):
    h = hashlib.md5(text.encode('utf-8')).digest()
    vec = [(b / 255.0) - 0.5 for b in h[:10]]
    norm = math.sqrt(sum(x*x for x in vec))
    return [x/norm for x in vec] if norm > 0 else vec

def cosine_similarity(v1, v2):
    return sum(x*y for x, y in zip(v1, v2))

@pytest.fixture(scope="module")
def expected_results():
    datasets = [
        {"id": "ds1", "description": "Global climate and weather patterns"},
        {"id": "ds2", "description": "Financial stock market historical data"},
        {"id": "ds3", "description": "Images of cats and dogs for classification"},
        {"id": "ds4", "description": "Text corpus of ancient Greek literature"},
        {"id": "ds5", "description": "Daily temperature and precipitation records"}
    ]

    query_vec = deterministic_embedding("climate")
    results = []
    for ds in datasets:
        ds_vec = deterministic_embedding(ds["description"])
        score = cosine_similarity(query_vec, ds_vec)
        results.append({"id": ds["id"], "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def test_search_endpoint(expected_results):
    try:
        response = requests.get("http://127.0.0.1:9000/search?q=climate&k=2", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the C++ service on port 9000: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from C++ service is not valid JSON")

    assert "results" in data, "'results' key missing in the JSON response"
    results = data["results"]
    assert isinstance(results, list), "'results' should be a list"
    assert len(results) == 2, f"Expected 2 results, got {len(results)}"

    for i in range(2):
        assert "id" in results[i], f"Result {i} missing 'id'"
        assert "score" in results[i], f"Result {i} missing 'score'"

        expected_id = expected_results[i]["id"]
        expected_score = expected_results[i]["score"]

        assert results[i]["id"] == expected_id, f"Expected id {expected_id} at rank {i+1}, got {results[i]['id']}"
        assert math.isclose(results[i]["score"], expected_score, abs_tol=1e-2), \
            f"Expected score ~{expected_score} at rank {i+1}, got {results[i]['score']}"

def test_benchmark_log():
    log_path = "/home/user/benchmark.log"
    assert os.path.isfile(log_path), f"Benchmark log file {log_path} is missing"

    with open(log_path, 'r') as f:
        content = f.read()

    # Look for the specific log entry
    pattern = r"\[climate\] time_ms:\s*([0-9]*\.?[0-9]+)"
    match = re.search(pattern, content)
    assert match is not None, f"Could not find the expected benchmark log pattern for 'climate' in {log_path}. Content: {content}"

    # Ensure it's a valid float
    try:
        float(match.group(1))
    except ValueError:
        pytest.fail(f"Logged time_ms value '{match.group(1)}' is not a valid float")