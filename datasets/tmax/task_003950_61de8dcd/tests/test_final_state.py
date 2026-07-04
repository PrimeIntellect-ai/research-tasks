# test_final_state.py
import os
import requests
import pytest
import math

def test_target_directory_exists():
    """Verify that the target directory exists."""
    path = "/home/user/dataset-catalog"
    assert os.path.isdir(path), f"Target directory {path} does not exist. Did you copy the package?"

def test_scorer_bayes_go_fixed():
    """Verify that the bayes.go file exists in the target directory."""
    path = "/home/user/dataset-catalog/scorer/bayes.go"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()
    # Check if the plus sign was replaced by a multiplication sign
    assert "(prior * likelihood)" in content or "prior*likelihood" in content or "prior * likelihood" in content, \
        "The mathematical bug in bayes.go does not appear to be fixed."

def test_service_running_and_correct():
    """Verify that the service is listening on 127.0.0.1:9090 and returns correct posterior."""
    url = "http://127.0.0.1:9090/score"

    # Test case 1 from truth
    params1 = {
        "prior": 0.4,
        "likelihood": 0.8,
        "marginal": 0.5
    }
    try:
        response1 = requests.get(url, params=params1, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}. Is it running in the background? Error: {e}")

    assert response1.status_code == 200, f"Expected HTTP 200 OK, got {response1.status_code}"

    try:
        data1 = response1.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response1.text}")

    assert "posterior" in data1, f"Expected 'posterior' in JSON response, got {data1}"
    assert math.isclose(data1["posterior"], 0.64, rel_tol=1e-5), \
        f"Expected posterior to be 0.64, got {data1['posterior']}. Is the math fixed?"

    # Test case 2 (dynamic check)
    params2 = {
        "prior": 0.3,
        "likelihood": 0.6,
        "marginal": 0.9
    }
    response2 = requests.get(url, params=params2, timeout=2)
    assert response2.status_code == 200
    data2 = response2.json()
    assert math.isclose(data2["posterior"], 0.2, rel_tol=1e-5), \
        f"Expected posterior to be 0.2, got {data2['posterior']}. Is the math fixed?"