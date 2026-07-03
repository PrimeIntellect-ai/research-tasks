# test_final_state.py

import pytest
import requests
import json

def solve_poisson_peak(Q, X=25, Y=30, size=50, tol=1e-4):
    """
    Reference Gauss-Seidel solver for Poisson equation on a 50x50 grid.
    Boundaries are 0.
    Returns the peak temperature.
    """
    grid = [[0.0 for _ in range(size)] for _ in range(size)]

    max_diff = tol + 1
    iters = 0
    while max_diff >= tol and iters < 10000:
        max_diff = 0.0
        for i in range(1, size - 1):
            for j in range(1, size - 1):
                old_val = grid[i][j]

                q_val = Q if (i == X and j == Y) else 0.0

                new_val = 0.25 * (grid[i+1][j] + grid[i-1][j] + grid[i][j+1] + grid[i][j-1] + q_val)
                grid[i][j] = new_val

                diff = abs(new_val - old_val)
                if diff > max_diff:
                    max_diff = diff
        iters += 1

    peak_T = 0.0
    for i in range(size):
        for j in range(size):
            if grid[i][j] > peak_T:
                peak_T = grid[i][j]

    return peak_T

def test_api_generate_endpoint():
    target = 75.0
    url = f"http://127.0.0.1:8080/generate?target={target}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or timeout: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    required_keys = {"Q", "a", "b", "c"}
    assert required_keys.issubset(data.keys()), f"JSON response missing required keys. Expected {required_keys}, got {list(data.keys())}"

    Q = float(data["Q"])
    a = float(data["a"])

    assert a < 0, f"Expected 'a' (quadratic term) to be strictly negative for a peak, got {a}"

    # Calculate peak T with the returned Q
    peak_T = solve_poisson_peak(Q, X=25, Y=30)

    assert abs(peak_T - target) <= 0.5, f"Returned Q={Q} produces peak T={peak_T}, which is not within ±0.5 of target {target}"