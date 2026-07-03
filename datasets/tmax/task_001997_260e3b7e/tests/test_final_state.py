# test_final_state.py

import os
import requests
import pytest

def test_server_binary_exists():
    path = "/home/user/server"
    assert os.path.isfile(path), f"Compiled server binary not found at {path}"
    assert os.access(path, os.X_OK), f"Server binary at {path} is not executable"

def test_coauthors_alice():
    url = "http://127.0.0.1:8080/coauthors?name=Alice"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("author") == "Alice", f"Expected author 'Alice', got {data.get('author')}"
    assert "coauthors" in data, "Response JSON missing 'coauthors' key"

    coauthors = data["coauthors"]
    assert isinstance(coauthors, list), f"Expected 'coauthors' to be a list, got {type(coauthors)}"

    # Charlie should be included (Paper 102, year 2022)
    # Bob should be excluded (Paper 101, year 2020)
    # David should be excluded (Paper 103, no shared paper)
    assert len(coauthors) == 1, f"Expected exactly 1 coauthor for Alice, got {len(coauthors)}: {coauthors}"
    assert "Charlie" in coauthors, f"Expected 'Charlie' in coauthors for Alice, got {coauthors}"

def test_coauthors_bob():
    url = "http://127.0.0.1:8080/coauthors?name=Bob"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()

    assert data.get("author") == "Bob"
    assert "coauthors" in data
    # Bob's only paper is in 2020, so he should have no valid coauthors based on the filter
    assert len(data["coauthors"]) == 0, f"Bob should have no coauthors from papers >= 2021, got {data['coauthors']}"

def test_coauthors_charlie():
    url = "http://127.0.0.1:8080/coauthors?name=Charlie"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200
    data = response.json()

    assert data.get("author") == "Charlie"
    assert "coauthors" in data
    assert len(data["coauthors"]) == 1, f"Expected exactly 1 coauthor for Charlie, got {len(data['coauthors'])}"
    assert "Alice" in data["coauthors"], f"Expected 'Alice' in coauthors for Charlie, got {data['coauthors']}"

def test_coauthors_david():
    url = "http://127.0.0.1:8080/coauthors?name=David"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200
    data = response.json()

    assert data.get("author") == "David"
    assert "coauthors" in data
    assert len(data["coauthors"]) == 0, f"David should have no coauthors, got {data['coauthors']}"