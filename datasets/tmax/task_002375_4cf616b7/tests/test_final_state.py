# test_final_state.py

import os
import time
import requests
import pytest

def test_ready_file_exists():
    """Verify that the user created the ready.txt file."""
    ready_file = "/app/ready.txt"
    assert os.path.isfile(ready_file), f"File {ready_file} does not exist. Did you signal readiness?"
    with open(ready_file, "r") as f:
        content = f.read().strip()
    assert "READY" in content, f"File {ready_file} does not contain 'READY'. Content: {content}"

def test_interactions_kinasea():
    """Verify the /interactions endpoint for KinaseA."""
    url = "http://127.0.0.1:8080/interactions?protein=KinaseA"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    expected = [
        {"relation": "activates", "target": "ProteaseB"},
        {"relation": "phosphorylates", "target": "ReceptorD"}
    ]

    # Sort both to ensure order doesn't fail if they implemented it differently, though spec says "sorted alphabetically by target"
    # Actually, spec requires sorting alphabetically by target protein's name.
    # The expected list is already sorted by target: ProteaseB, ReceptorD.
    assert data == expected, f"Expected {expected}, got {data}"

def test_interactions_factorc():
    """Verify the /interactions endpoint for FactorC."""
    url = "http://127.0.0.1:8080/interactions?protein=FactorC"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    expected = [
        {"relation": "activates", "target": "KinaseA"}
    ]

    assert data == expected, f"Expected {expected}, got {data}"

def test_interactions_empty():
    """Verify the /interactions endpoint for a non-existent protein."""
    url = "http://127.0.0.1:8080/interactions?protein=UnknownProteinX"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    assert data == [], f"Expected empty array [], got {data}"

def test_export():
    """Verify the /export endpoint."""
    url = "http://127.0.0.1:8080/export"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    expected = [
      {"source": "FactorC", "relation": "activates", "target": "KinaseA"},
      {"source": "KinaseA", "relation": "activates", "target": "ProteaseB"},
      {"source": "KinaseA", "relation": "phosphorylates", "target": "ReceptorD"},
      {"source": "ProteaseB", "relation": "inhibits", "target": "FactorC"},
      {"source": "ReceptorD", "relation": "inhibits", "target": "ProteaseB"}
    ]

    assert data == expected, f"Expected {expected}, got {data}"