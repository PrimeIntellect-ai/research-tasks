# test_final_state.py
import os
import requests
import pytest
import math

def test_cxxopts_fixed():
    """Verify that the student fixed the cxxopts.hpp header by adding <string>."""
    header_path = "/app/vendored/cxxopts/include/cxxopts.hpp"
    assert os.path.isfile(header_path), f"Vendored header not found at {header_path}"
    with open(header_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "#include <string>" in content, "The file cxxopts.hpp is still missing '#include <string>'."

def test_server_running_and_evaluates_math():
    """Verify that the server is running on port 8080 and evaluates math correctly."""
    url = "http://127.0.0.1:8080/score"

    test_cases = [
        {"data": {"expr": "3*x^2+2*x-5", "x": "4.5"}, "expected": 64.75},
        {"data": {"expr": "(x+2)*(x-3)", "x": "10"}, "expected": 84.0},
        {"data": {"expr": "2*x^2+3*x-1", "x": "5"}, "expected": 64.0},
    ]

    for case in test_cases:
        try:
            response = requests.post(url, data=case["data"], timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the server at {url} or request failed: {e}")

        assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

        try:
            result = float(response.text.strip())
        except ValueError:
            pytest.fail(f"Expected a numerical string response, got: {response.text}")

        assert math.isclose(result, case["expected"], rel_tol=1e-5), \
            f"Evaluation failed for {case['data']}. Expected {case['expected']}, got {result}"