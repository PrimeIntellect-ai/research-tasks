# test_final_state.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:9090"
HEADERS = {"X-Bio-Auth": "secret-token-77"}

def test_unauthorized():
    """Test that requests without the correct auth header return 401."""
    try:
        response = requests.get(f"{BASE_URL}/slope/0/0", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

@pytest.mark.parametrize("x, y, expected_slope", [
    (0, 0, "10.00"),
    (1, 0, "20.00"),
    (0, 1, "5.00"),
    (1, 1, "0.00"),
])
def test_slope_endpoints(x, y, expected_slope):
    """Test that authenticated requests return the correct slope."""
    try:
        response = requests.get(f"{BASE_URL}/slope/{x}/{y}", headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK for /slope/{x}/{y}, got {response.status_code}"

    actual_slope = response.text.strip()
    assert actual_slope == expected_slope, f"Expected slope {expected_slope} for /slope/{x}/{y}, got '{actual_slope}'"