# test_final_state.py

import os
import pytest
import requests

URL = "http://127.0.0.1:8000/api/v1/analyze_path"

def test_fixture_script_exists():
    path = "/home/user/test_fixture.py"
    assert os.path.isfile(path), f"The test fixture script at {path} is missing or not a file."

def test_api_guest_pivot_denied():
    payload = {
        "nodes": {"n1": "PublicPage", "n2": "UserDashboard"},
        "edges": [["n1", "n2"]],
        "source": "n1",
        "target": "n2",
        "token": "GUEST"
    }
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("path_exists") is False, f"Expected 'path_exists': False for GUEST token, got {data}"

def test_api_user_pivot_allowed():
    payload = {
        "nodes": {"n1": "PublicPage", "n2": "UserDashboard"},
        "edges": [["n1", "n2"]],
        "source": "n1",
        "target": "n2",
        "token": "USER_TOKEN"
    }
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("path_exists") is True, f"Expected 'path_exists': True for USER_TOKEN on valid path, got {data}"

def test_api_user_pivot_denied():
    payload = {
        "nodes": {"n1": "PublicPage", "n2": "UserDashboard", "n3": "AdminPanel"},
        "edges": [["n1", "n2"], ["n2", "n3"]],
        "source": "n1",
        "target": "n3",
        "token": "USER_TOKEN"
    }
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("path_exists") is False, f"Expected 'path_exists': False for USER_TOKEN to AdminPanel, got {data}"

def test_api_superadmin_pivot_allowed():
    payload = {
        "nodes": {"n1": "PublicPage", "n2": "UserDashboard", "n3": "AdminPanel", "n4": "SecretDB"},
        "edges": [["n1", "n2"], ["n2", "n3"], ["n3", "n4"]],
        "source": "n1",
        "target": "n4",
        "token": "SUPERADMIN"
    }
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("path_exists") is True, f"Expected 'path_exists': True for SUPERADMIN token, got {data}"

def test_api_complex_graph_traversal():
    # Graph with two paths: one invalid (via AdminPanel), one valid (via UserDashboard)
    payload = {
        "nodes": {
            "start": "PublicPage",
            "mid1": "AdminPanel",
            "mid2": "UserDashboard",
            "end": "PublicPage"
        },
        "edges": [
            ["start", "mid1"],
            ["mid1", "end"],
            ["start", "mid2"],
            ["mid2", "end"]
        ],
        "source": "start",
        "target": "end",
        "token": "USER_TOKEN"
    }
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("path_exists") is True, f"Expected 'path_exists': True for complex graph with valid alternative path, got {data}"