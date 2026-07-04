# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_record_endpoint_id_1():
    response = requests.get(f"{BASE_URL}/record?id=1", timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert "id" in data, "Response missing 'id' field"
    assert "token_count" in data, "Response missing 'token_count' field"
    assert "pca_1" in data, "Response missing 'pca_1' field"
    assert "pca_2" in data, "Response missing 'pca_2' field"

    # Verify id is strictly an integer
    assert isinstance(data["id"], int), f"Expected 'id' to be int, got {type(data['id'])}"
    assert data["id"] == 1, f"Expected id to be 1, got {data['id']}"

    # Verify token count for id 1 ('this is a test record' -> 5)
    assert data["token_count"] == 5, f"Expected token_count 5, got {data['token_count']}"

    # Verify pca fields are floats
    assert isinstance(data["pca_1"], float), f"Expected 'pca_1' to be float, got {type(data['pca_1'])}"
    assert isinstance(data["pca_2"], float), f"Expected 'pca_2' to be float, got {type(data['pca_2'])}"

def test_record_endpoint_id_2():
    response = requests.get(f"{BASE_URL}/record?id=2", timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert data["id"] == 2
    assert isinstance(data["id"], int)

    # Verify token count for id 2 ('another test record with more words' -> 6)
    assert data["token_count"] == 6

def test_record_endpoint_id_3():
    response = requests.get(f"{BASE_URL}/record?id=3", timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert data["id"] == 3
    assert isinstance(data["id"], int)

    # Verify token count for id 3 ('short text' -> 2)
    assert data["token_count"] == 2

def test_benchmark_endpoint():
    response = requests.get(f"{BASE_URL}/benchmark", timeout=30)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    data = response.json()
    assert "avg_inference_time_ms" in data, "Response missing 'avg_inference_time_ms' field"
    assert isinstance(data["avg_inference_time_ms"], float), f"Expected float, got {type(data['avg_inference_time_ms'])}"
    assert data["avg_inference_time_ms"] > 0, "Average inference time should be greater than 0"