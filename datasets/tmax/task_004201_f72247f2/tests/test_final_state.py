# test_final_state.py

import math
import pytest
import requests

def test_embedding_api():
    url = "http://127.0.0.1:8080/embed"
    payload = {"text": "The quick brown fox"}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to embedding API on port 8080: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Embedding API did not return valid JSON. Response: {response.text}")

    assert "embedding" in data, f"Response JSON is missing 'embedding' key. Got: {data}"
    emb = data["embedding"]
    assert isinstance(emb, list) and len(emb) == 3, f"Expected embedding to be a list of 3 floats, got {emb}"

    expected_emb = [0.63, 0.44, 0.9]
    for actual, expected in zip(emb, expected_emb):
        assert math.isclose(actual, expected, abs_tol=1e-5), f"Expected embedding {expected_emb}, got {emb}"

def test_results_api():
    url = "http://127.0.0.1:8081/results"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to results API on port 8081: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Results API did not return valid JSON. Response: {response.text}")

    assert "correlation_matrix" in data, f"Missing 'correlation_matrix' in response. Got: {data}"
    assert "benchmark_average_latency_sec" in data, f"Missing 'benchmark_average_latency_sec' in response. Got: {data}"

    latency = data["benchmark_average_latency_sec"]
    assert isinstance(latency, (int, float)), f"Latency must be a number, got {type(latency)}"
    assert latency > 0, f"Latency must be greater than 0, got {latency}"

    # Compute expected matrix
    def get_embedding(text):
        length = len(text)
        v1 = sum(ord(c) for c in text) % 100 / 100.0
        v2 = sum(ord(c) * i for i, c in enumerate(text)) % 100 / 100.0
        v3 = length % 10 / 10.0
        return [v1, v2, v3]

    sentences = [
        "The quick brown fox",
        "Jumps over the lazy dog",
        "Machine learning is fascinating",
        "Data science requires statistical thinking",
        "Artificial intelligence agents",
        "Building multi-protocol verifiers",
        "Terminal environments for bash"
    ]

    embeddings = [get_embedding(s) for s in sentences]

    def pearson_corr(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        den_x = sum((xi - mean_x)**2 for xi in x)
        den_y = sum((yi - mean_y)**2 for yi in y)
        if den_x == 0 or den_y == 0:
            return 0.0
        return num / math.sqrt(den_x * den_y)

    expected_matrix = []
    for i in range(3):
        row = []
        for j in range(3):
            col_i = [e[i] for e in embeddings]
            col_j = [e[j] for e in embeddings]
            row.append(pearson_corr(col_i, col_j))
        expected_matrix.append(row)

    actual_matrix = data["correlation_matrix"]
    assert isinstance(actual_matrix, list) and len(actual_matrix) == 3, f"Matrix must be a list of 3 lists, got {actual_matrix}"
    for i in range(3):
        assert isinstance(actual_matrix[i], list) and len(actual_matrix[i]) == 3, f"Matrix row {i} must have 3 elements"
        for j in range(3):
            assert math.isclose(actual_matrix[i][j], expected_matrix[i][j], abs_tol=0.002), \
                f"Mismatch in correlation matrix at ({i},{j}): expected {expected_matrix[i][j]:.4f}, got {actual_matrix[i][j]}"