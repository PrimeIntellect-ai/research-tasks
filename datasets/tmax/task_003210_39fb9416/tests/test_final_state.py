# test_final_state.py

import os
import json
import pytest
import requests
import time

def test_target_sequence_file():
    path = "/app/target_sequence.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "ACTGGCCTTAACGGAT", f"Expected target sequence 'ACTGGCCTTAACGGAT', but got '{content}'."

def test_regression_notebook_executed():
    path = "/app/regression.ipynb"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not a valid JSON/Jupyter notebook.")

    executed = False
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            if cell.get("execution_count") is not None:
                executed = True
                break

    assert executed, f"The notebook {path} does not appear to have been executed (no execution counts found)."

def test_bash_optimization_service_16():
    url = "http://127.0.0.1:8080/optimize?min_len=16"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the optimization service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "ID_001" in response.text, f"Expected 'ID_001' in response, got '{response.text}'"

def test_bash_optimization_service_18():
    url = "http://127.0.0.1:8080/optimize?min_len=18"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the optimization service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "ID_005" in response.text, f"Expected 'ID_005' in response, got '{response.text}'"

def test_bash_optimization_service_14():
    url = "http://127.0.0.1:8080/optimize?min_len=14"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the optimization service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "ID_001" in response.text, f"Expected 'ID_001' in response, got '{response.text}'"