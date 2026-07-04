# test_final_state.py
import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:8080/compute"

def get_compute(input_str):
    try:
        resp = requests.get(f"{BASE_URL}?input={input_str}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API Gateway at {BASE_URL}. Are nginx and the compute-engine running? Error: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response: {resp.text}")

    assert "mean" in data, f"Missing 'mean' key in response: {data}"
    assert "variance" in data, f"Missing 'variance' key in response: {data}"
    return data

def test_numerical_stability():
    """Test 1: Numerical Stability & Precision"""
    data = get_compute("100000000.0,100000001.0,100000002.0")
    assert math.isclose(data["mean"], 100000001.0, rel_tol=1e-5), f"Expected mean 100000001.0, got {data['mean']}"
    assert math.isclose(data["variance"], 1.0, rel_tol=1e-5), f"Expected variance 1.0, got {data['variance']}. Check numerical stability (f64 vs f32)."

def test_format_parsing_edge_cases():
    """Test 2: Format Parsing Edge Case"""
    data = get_compute("10.0,NaN,invalid,N/A,20.0")
    assert math.isclose(data["mean"], 15.0, rel_tol=1e-5), f"Expected mean 15.0, got {data['mean']}"
    assert math.isclose(data["variance"], 25.0, rel_tol=1e-5), f"Expected variance 25.0, got {data['variance']}. Ensure invalid/NaN strings are filtered out."

def test_single_valid_value():
    """Test 3: Single valid value"""
    data = get_compute("42.0,NaN")
    assert math.isclose(data["mean"], 42.0, rel_tol=1e-5), f"Expected mean 42.0, got {data['mean']}"
    assert math.isclose(data["variance"], 0.0, rel_tol=1e-5), f"Expected variance 0.0, got {data['variance']}. Variance for < 2 valid points should be 0.0."