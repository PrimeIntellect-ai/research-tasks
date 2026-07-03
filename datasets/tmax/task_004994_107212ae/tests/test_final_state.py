# test_final_state.py
import subprocess
import requests
import pytest

def test_pde_solver():
    url = "http://127.0.0.1:8080/solve"
    payload = {"id": "test_verification", "alpha": 0.1, "t_end": 0.1}

    try:
        response = requests.post(url, json=payload, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service on port 8080 or request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response: {response.text}"

    try:
        result = subprocess.run(
            ["redis-cli", "LRANGE", "solution:test_verification", "0", "-1"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Redis: {e.stderr}")

    lines = result.stdout.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    assert len(lines) == 11, f"Expected 11 elements in Redis list 'solution:test_verification', got {len(lines)}: {lines}"

    try:
        values = [float(x) for x in lines]
    except ValueError as e:
        pytest.fail(f"Failed to parse Redis list values as floats: {e}")

    assert abs(values[0]) < 1e-6, f"Expected first element to be 0.0, got {values[0]}"
    assert abs(values[-1]) < 1e-6, f"Expected last element to be 0.0, got {values[-1]}"

    midpoint = values[5]
    assert 0.720 <= midpoint <= 0.730, f"Expected midpoint (index 5) to be between 0.720 and 0.730, got {midpoint}"