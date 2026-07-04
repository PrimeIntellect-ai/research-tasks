# test_final_state.py
import pytest
import requests
import subprocess
import math

def get_oracle_root(a, b, c, d):
    try:
        result = subprocess.run(
            ["/app/oracle_solver", str(a), str(b), str(c), str(d)],
            capture_output=True,
            text=True,
            check=True
        )
        # Assuming the oracle outputs the float value directly
        output = result.stdout.strip()
        # Find the last word that looks like a float if there's extra text
        words = output.split()
        for word in reversed(words):
            try:
                return float(word)
            except ValueError:
                continue
        return float(output)
    except Exception as e:
        pytest.fail(f"Failed to run oracle solver for {a} {b} {c} {d}: {e}")

test_cases = [
    (1.0, -6.0, 11.0, -6.0),
    (1.0, 0.0, 0.0, -8.0),
    (1.0, 1000.0, 1000.0, 1000.0), # Potential precision issue case
    (2.0, -4.0, -22.0, 24.0),
    (1.0, 0.0, 1.0, 0.0),
    (1.0, 3.0, 3.0, 1.0),
]

@pytest.mark.parametrize("a, b, c, d", test_cases)
def test_solve_endpoint(a, b, c, d):
    expected_root = get_oracle_root(a, b, c, d)

    url = "http://127.0.0.1:8080/solve"
    payload = {"a": a, "b": b, "c": c, "d": d}

    try:
        response = requests.post(url, json=payload, timeout=3.0)
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {url} timed out for inputs {payload}. The infinite loop bug might not be fixed.")
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Failed to connect to {url}. Is the server running on port 8080?")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse JSON response: {response.text}")

    assert "root" in data, f"Response JSON missing 'root' key: {data}"

    actual_root = data["root"]
    assert isinstance(actual_root, (int, float)), f"Expected 'root' to be a number, got {type(actual_root)}"

    tolerance = 1e-5
    assert math.isclose(actual_root, expected_root, abs_tol=tolerance), \
        f"For inputs {payload}, expected root ~{expected_root}, but got {actual_root} (diff: {abs(actual_root - expected_root)})"