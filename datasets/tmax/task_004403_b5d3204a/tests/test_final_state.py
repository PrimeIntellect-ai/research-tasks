# test_final_state.py
import os
import requests
import time
import pytest

def test_nginx_proxy_unauthorized():
    """Test that requests without the correct Authorization header are rejected with 401."""
    url = "http://localhost:8080/api/fit"

    # Missing header
    response = requests.get(url)
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

    # Incorrect header
    headers = {"Authorization": "Bearer WRONG_TOKEN"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, f"Expected 401 Unauthorized for wrong token, got {response.status_code}"

def test_nginx_proxy_authorized_and_deterministic():
    """Test that authorized requests return 200 and the output is deterministic across multiple calls."""
    url = "http://localhost:8080/api/fit"
    headers = {"Authorization": "Bearer BOOTSTRAP_SECURE_99"}

    results = []
    for i in range(5):
        try:
            response = requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request {i+1} failed: {e}")

        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
        results.append(response.text.strip())

    # Check determinism
    first_result = results[0]
    for i, res in enumerate(results[1:], start=2):
        assert res == first_result, f"Non-deterministic output detected. Request 1 gave '{first_result}', but Request {i} gave '{res}'"

    # Basic format check: [lower, upper]
    assert first_result.startswith("[") and first_result.endswith("]"), f"Output format incorrect: {first_result}"
    parts = first_result[1:-1].split(",")
    assert len(parts) == 2, f"Expected two values in output, got: {first_result}"
    try:
        lower = float(parts[0].strip())
        upper = float(parts[1].strip())
        assert lower < upper, f"Lower bound {lower} is not less than upper bound {upper}"
    except ValueError:
        pytest.fail(f"Could not parse floats from output: {first_result}")

def test_success_log_exists():
    """Test that the success.log file was created and contains the expected format."""
    log_path = "/home/user/app/success.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content.startswith("[") and content.endswith("]"), f"success.log content format incorrect: {content}"