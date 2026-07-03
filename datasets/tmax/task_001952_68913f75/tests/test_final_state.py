# test_final_state.py
import math
import subprocess
import requests
import pytest

def get_oracle_result(y1, y2, y3, t_end):
    cmd = ["/app/chemical_oracle", str(y1), str(y2), str(y3), str(t_end)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    output = result.stdout.strip()
    parts = output.split()
    if len(parts) != 3:
        raise ValueError(f"Oracle returned unexpected output: {output}")
    return [float(x) for x in parts]

@pytest.mark.parametrize("y1, y2, y3, t_end", [
    (1.0, 0.0, 0.0, 0.4),
    (1.0, 0.0, 0.0, 40.0),
    (1.0, 0.0, 0.0, 400.0),
    (0.5, 0.1, 0.4, 10.0),
])
def test_simulate_endpoint(y1, y2, y3, t_end):
    # Get expected result from oracle
    expected_y = get_oracle_result(y1, y2, y3, t_end)

    # Query the student's API
    url = "http://127.0.0.1:8080/simulate"
    payload = {
        "y0": [y1, y2, y3],
        "t_end": t_end
    }

    try:
        response = requests.post(url, json=payload, timeout=5.0)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "y_final" in data, f"Missing 'y_final' in response: {data}"

    actual_y = data["y_final"]
    assert isinstance(actual_y, list) and len(actual_y) == 3, f"Expected 'y_final' to be a list of 3 floats, got: {actual_y}"

    # Compare results
    for i, (act, exp) in enumerate(zip(actual_y, expected_y)):
        # Using a relative tolerance of 1e-4 and a small absolute tolerance for values close to zero
        assert math.isclose(act, exp, rel_tol=1e-4, abs_tol=1e-9), \
            f"Mismatch at index {i} for input y0={payload['y0']}, t_end={t_end}. Expected {exp}, got {act}"