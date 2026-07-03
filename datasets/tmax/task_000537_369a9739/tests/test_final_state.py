# test_final_state.py

import os
import json
import pytest
import requests

def test_prot_integrator_bug_fixed():
    path = "/app/prot_integrator/prot_integrator/core.py"
    assert os.path.isfile(path), f"Expected file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "dt = dt * 1.5" not in content and "dt *= 1.5" not in content, \
        f"The deliberate bug 'dt = dt * 1.5' is still present in {path}."

def test_workflow_notebook_exists():
    path = "/home/user/workflow.ipynb"
    assert os.path.isfile(path), f"Expected Jupyter notebook {path} does not exist."
    with open(path, "r") as f:
        try:
            nb = json.load(f)
            assert "cells" in nb, f"File {path} does not appear to be a valid Jupyter notebook."
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

def test_api_unauthorized_missing_token():
    url = "http://127.0.0.1:8080/api/v1/stats?pdb=1A2B"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}."

def test_api_unauthorized_invalid_token():
    url = "http://127.0.0.1:8080/api/v1/stats?pdb=1A2B"
    headers = {"Authorization": "Bearer wrong_token"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {response.status_code}."

def test_api_authorized_success():
    url = "http://127.0.0.1:8080/api/v1/stats?pdb=1A2B"
    headers = {"Authorization": "Bearer dev_token_99x"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for valid token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "pdb_id" in data, "Response JSON missing 'pdb_id' key."
    assert data["pdb_id"] == "1A2B", f"Expected pdb_id '1A2B', got {data['pdb_id']}."

    assert "ci_lower" in data, "Response JSON missing 'ci_lower' key."
    assert "ci_upper" in data, "Response JSON missing 'ci_upper' key."

    assert isinstance(data["ci_lower"], (int, float)), "ci_lower must be a number."
    assert isinstance(data["ci_upper"], (int, float)), "ci_upper must be a number."
    assert data["ci_lower"] <= data["ci_upper"], "ci_lower must be less than or equal to ci_upper."