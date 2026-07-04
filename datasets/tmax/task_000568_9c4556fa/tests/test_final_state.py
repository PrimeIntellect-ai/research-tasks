# test_final_state.py
import requests
import math
import pytest

def compute_expected(data):
    # Extract valid points
    valid_points = [d for d in data if d.get("B") is not None]

    # Linear Regression B on A
    n_valid = len(valid_points)
    mean_a = sum(d["A"] for d in valid_points) / n_valid
    mean_b = sum(d["B"] for d in valid_points) / n_valid

    num = sum((d["A"] - mean_a) * (d["B"] - mean_b) for d in valid_points)
    den = sum((d["A"] - mean_a) ** 2 for d in valid_points)

    beta_1 = num / den
    beta_0 = mean_b - beta_1 * mean_a

    # Impute missing
    imputed_b = []
    for d in data:
        if d.get("B") is not None:
            imputed_b.append(d["B"])
        else:
            imputed_b.append(beta_0 + beta_1 * d["A"])

    # Calculate CI
    n_total = len(imputed_b)
    mean_b_full = sum(imputed_b) / n_total
    variance = sum((b - mean_b_full) ** 2 for b in imputed_b) / (n_total - 1)
    stddev = math.sqrt(variance)

    se = stddev / math.sqrt(n_total)
    moe = 1.96 * se

    ci_lower = mean_b_full - moe
    ci_upper = mean_b_full + moe

    return imputed_b, ci_lower, ci_upper

def test_service_payload_1():
    payload = {
        "data": [
            {"A": 10.0, "B": 15.0},
            {"A": 12.0, "B": 20.0},
            {"A": 15.0, "B": None},
            {"A": 18.0, "B": 35.0},
            {"A": 20.0, "B": None}
        ]
    }

    try:
        response = requests.post("http://127.0.0.1:9090/clean", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service on 127.0.0.1:9090. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        result = response.json()
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {response.text}. Error: {e}")

    expected_b, expected_lower, expected_upper = compute_expected(payload["data"])

    assert "imputed_B" in result, "Response missing 'imputed_B' key"
    assert "ci_lower" in result, "Response missing 'ci_lower' key"
    assert "ci_upper" in result, "Response missing 'ci_upper' key"

    assert len(result["imputed_B"]) == len(expected_b), "Length of imputed_B does not match expected"
    for act, exp in zip(result["imputed_B"], expected_b):
        assert math.isclose(act, exp, abs_tol=1e-3), f"Imputed value {act} does not match expected {exp}"

    assert math.isclose(result["ci_lower"], expected_lower, abs_tol=1e-3), f"ci_lower {result['ci_lower']} does not match expected {expected_lower}"
    assert math.isclose(result["ci_upper"], expected_upper, abs_tol=1e-3), f"ci_upper {result['ci_upper']} does not match expected {expected_upper}"

def test_service_payload_2():
    payload = {
        "data": [
            {"A": 1.0, "B": 2.0},
            {"A": 2.0, "B": None},
            {"A": 3.0, "B": 6.0}
        ]
    }

    try:
        response = requests.post("http://127.0.0.1:9090/clean", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service on 127.0.0.1:9090. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        result = response.json()
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {response.text}. Error: {e}")

    expected_b, expected_lower, expected_upper = compute_expected(payload["data"])

    assert "imputed_B" in result, "Response missing 'imputed_B' key"
    assert "ci_lower" in result, "Response missing 'ci_lower' key"
    assert "ci_upper" in result, "Response missing 'ci_upper' key"

    assert len(result["imputed_B"]) == len(expected_b), "Length of imputed_B does not match expected"
    for act, exp in zip(result["imputed_B"], expected_b):
        assert math.isclose(act, exp, abs_tol=1e-3), f"Imputed value {act} does not match expected {exp}"

    assert math.isclose(result["ci_lower"], expected_lower, abs_tol=1e-3), f"ci_lower {result['ci_lower']} does not match expected {expected_lower}"
    assert math.isclose(result["ci_upper"], expected_upper, abs_tol=1e-3), f"ci_upper {result['ci_upper']} does not match expected {expected_upper}"