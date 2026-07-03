# test_final_state.py

import os
import time
import pytest
import requests

def test_database_directory_exists():
    """Verify that the Kùzu database directory was created."""
    db_path = "/home/user/graph_db"
    assert os.path.isdir(db_path), f"Database directory {db_path} does not exist."

def test_api_log_exists():
    """Verify that the API log file was created."""
    log_path = "/home/user/api.log"
    assert os.path.isfile(log_path), f"API log file {log_path} does not exist."

def test_api_query_e101():
    """Test the POST /query endpoint for employee E101."""
    url = "http://127.0.0.1:8080/query"
    payload = {"employee_id": "E101"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "projects" in data, f"Response JSON missing 'projects' key: {data}"

    expected_projects = {"Project Titan", "Project Apollo"}
    actual_projects = set(data["projects"])

    assert actual_projects == expected_projects, f"Expected projects {expected_projects}, got {actual_projects}"

def test_api_query_e102():
    """Test the POST /query endpoint for employee E102."""
    url = "http://127.0.0.1:8080/query"
    payload = {"employee_id": "E102"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "projects" in data, f"Response JSON missing 'projects' key: {data}"

    expected_projects = {"Project Titan"}
    actual_projects = set(data["projects"])

    assert actual_projects == expected_projects, f"Expected projects {expected_projects}, got {actual_projects}"