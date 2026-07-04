# test_final_state.py

import os
import json
import requests
import time

def test_files_exist_and_valid():
    index_path = "/home/user/faiss_index.bin"
    chunks_path = "/home/user/chunks.json"

    assert os.path.isfile(index_path), f"FAISS index file missing at {index_path}"
    assert os.path.getsize(index_path) > 0, f"FAISS index file at {index_path} is empty"

    assert os.path.isfile(chunks_path), f"Chunks file missing at {chunks_path}"

    with open(chunks_path, "r") as f:
        try:
            chunks = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {chunks_path} is not valid JSON"

    assert isinstance(chunks, list), f"Chunks file {chunks_path} must contain a JSON array"
    assert len(chunks) > 0, "Chunks array is empty"
    assert all(isinstance(c, str) for c in chunks), "All items in chunks array must be strings"

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/search"
    headers = {"Authorization": "Bearer wrong-token"}
    payload = {"query": "test"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to API on 127.0.0.1:8080: {e}"

    assert response.status_code == 401, f"Expected 401 Unauthorized for wrong token, got {response.status_code}"

def test_api_authorized_and_retrieval():
    url = "http://127.0.0.1:8080/search"
    headers = {"Authorization": "Bearer etl-secure-token-2024"}
    payload = {"query": "restarting the router device"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to API on 127.0.0.1:8080: {e}"

    assert response.status_code == 200, f"Expected 200 OK for valid token, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        assert False, "Response is not valid JSON"

    assert "best_match" in data, "Response JSON must contain 'best_match' key"

    best_match = data["best_match"].lower()

    # Check if the sentence roughly matches the expected one
    expected_keywords = ["unplugging", "power", "cable", "plugging"]
    matched_keywords = [kw for kw in expected_keywords if kw in best_match]

    assert len(matched_keywords) >= 2, f"Retrieved chunk does not seem to match the expected answer. Got: {data['best_match']}"