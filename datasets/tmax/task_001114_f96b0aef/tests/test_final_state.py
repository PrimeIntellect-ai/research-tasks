# test_final_state.py
import math
import requests
import pytest

def get_expected_sv(N):
    """
    Computes the dominant singular value of the matrix A[i,j] = sin(i*j*0.01)
    using power iteration. Since A is symmetric, the dominant singular value
    is the absolute value of the dominant eigenvalue.
    """
    v = [1.0] * N
    # Power iteration
    for _ in range(50):
        v_new = [0.0] * N
        for i in range(N):
            for j in range(N):
                v_new[i] += math.sin(i * j * 0.01) * v[j]
        norm = math.sqrt(sum(x * x for x in v_new))
        if norm == 0:
            break
        v = [x / norm for x in v_new]

    # Rayleigh quotient
    num = 0.0
    for i in range(N):
        row_dot = sum(math.sin(i * j * 0.01) * v[j] for j in range(N))
        num += v[i] * row_dot
    return abs(num)

def test_run_sim_endpoint_n100():
    url = "http://127.0.0.1:8080/run_sim"
    payload = {"mesh_size": 100}

    try:
        response = requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "dominant_singular_value" in data, f"Response JSON missing 'dominant_singular_value' key. Got: {data}"

    actual_sv = data["dominant_singular_value"]
    expected_sv = get_expected_sv(100)

    assert abs(actual_sv - expected_sv) < 1e-2, f"Dominant singular value mismatch for N=100. Expected ~{expected_sv}, got {actual_sv}"

def test_run_sim_endpoint_n50():
    url = "http://127.0.0.1:8080/run_sim"
    payload = {"mesh_size": 50}

    try:
        response = requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "dominant_singular_value" in data, f"Response JSON missing 'dominant_singular_value' key. Got: {data}"

    actual_sv = data["dominant_singular_value"]
    expected_sv = get_expected_sv(50)

    assert abs(actual_sv - expected_sv) < 1e-2, f"Dominant singular value mismatch for N=50. Expected ~{expected_sv}, got {actual_sv}"