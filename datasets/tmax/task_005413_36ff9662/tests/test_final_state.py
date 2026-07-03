# test_final_state.py
import pytest
import requests
import json
import math

def matrix_mult(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    C = [[0.0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_scale(A, scalar):
    return [[A[i][j] * scalar for j in range(len(A[0]))] for i in range(len(A))]

def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def matrix_exp(A, terms=50):
    n = len(A)
    result = eye(n)
    term = eye(n)
    for i in range(1, terms):
        term = matrix_mult(term, A)
        term = matrix_scale(term, 1.0 / i)
        result = matrix_add(result, term)
    return result

def test_unauthorized():
    url = "http://127.0.0.1:8080/simulate"
    payload = {
        "edges": [[0, 1], [0, 2], [0, 3]],
        "initial_state": [1.0, 0.0, 0.0, 0.0],
        "t_end": 2.0,
        "tol": 1e-4
    }

    # Missing header
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:8080. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}"

    # Incorrect token
    headers = {"Authorization": "Bearer wrong_token"}
    response = requests.post(url, json=payload, headers=headers, timeout=5)
    assert response.status_code == 401, f"Expected 401 Unauthorized for incorrect token, got {response.status_code}"

def test_simulate_endpoint():
    url = "http://127.0.0.1:8080/simulate"
    payload = {
        "edges": [[0, 1], [0, 2], [0, 3]],
        "initial_state": [1.0, 0.0, 0.0, 0.0],
        "t_end": 2.0,
        "tol": 1e-4
    }
    headers = {"Authorization": "Bearer sim_token_99"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:8080. Is it running?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "final_state" in data, "Response JSON missing 'final_state' key"

    final_state = data["final_state"]
    assert isinstance(final_state, list), "'final_state' must be a list"
    assert len(final_state) == 4, "'final_state' must have 4 elements"

    # Compute analytical solution
    L = [[ 3.0, -1.0, -1.0, -1.0],
         [-1.0,  1.0,  0.0,  0.0],
         [-1.0,  0.0,  1.0,  0.0],
         [-1.0,  0.0,  0.0,  1.0]]

    t_end = 2.0
    minus_Lt = matrix_scale(L, -t_end)
    exp_minus_Lt = matrix_exp(minus_Lt, terms=100)

    initial_state_col = [[1.0], [0.0], [0.0], [0.0]]
    true_final_state_col = matrix_mult(exp_minus_Lt, initial_state_col)
    true_final_state = [row[0] for row in true_final_state_col]

    for i in range(4):
        assert abs(final_state[i] - true_final_state[i]) <= 1e-3, \
            f"Element {i} mismatch: expected {true_final_state[i]:.4f}, got {final_state[i]:.4f}"