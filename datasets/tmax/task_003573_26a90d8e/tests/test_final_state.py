# test_final_state.py
import os
import json
import csv
import math
import requests
import pytest

API_URL = "http://127.0.0.1:8080"
HEADERS = {"Authorization": "Bearer ds-auth-token-999"}

def test_exp_results_exists():
    assert os.path.isfile("/home/user/exp_results.json"), "exp_results.json is missing."
    with open("/home/user/exp_results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("exp_results.json is not valid JSON.")
        assert isinstance(data, dict), "exp_results.json should contain a JSON object."

def test_api_unauthorized():
    try:
        r_pca = requests.get(f"{API_URL}/pca", timeout=5)
        r_test = requests.get(f"{API_URL}/test", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert r_pca.status_code == 401, f"Expected 401 for /pca without token, got {r_pca.status_code}"
    assert r_test.status_code == 401, f"Expected 401 for /test without token, got {r_test.status_code}"

def test_api_pca():
    try:
        r = requests.get(f"{API_URL}/pca", headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert r.status_code == 200, f"Expected 200 OK for /pca, got {r.status_code}. Body: {r.text}"
    data = r.json()
    assert "top_component" in data, "Response missing 'top_component' key."
    assert isinstance(data["top_component"], list), "'top_component' must be a list."
    assert len(data["top_component"]) == 5, f"Expected 5 elements in PCA vector, got {len(data['top_component'])}"
    for val in data["top_component"]:
        assert isinstance(val, (int, float)), "PCA vector elements must be numbers."

def test_api_test():
    try:
        r = requests.get(f"{API_URL}/test", headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert r.status_code == 200, f"Expected 200 OK for /test, got {r.status_code}. Body: {r.text}"
    data = r.json()
    for key in ["p_value", "ci_lower", "ci_upper"]:
        assert key in data, f"Response missing '{key}' key."
        assert isinstance(data[key], (int, float)), f"'{key}' must be a number."

def test_makefile_fixed():
    makefile_path = "/app/vendor/ml_prep_lib-0.1.0/Makefile"
    assert os.path.isfile(makefile_path), f"File {makefile_path} is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "pip install ." in content, "Makefile does not contain the fixed 'pip install .' command."

def test_core_py_fixed():
    core_py_path = "/app/vendor/ml_prep_lib-0.1.0/ml_prep_lib/core.py"
    assert os.path.isfile(core_py_path), f"File {core_py_path} is missing."
    with open(core_py_path, "r") as f:
        content = f.read()
    assert "Int64" in content, "core.py does not seem to use 'Int64' to fix the precision loss issue."