# test_final_state.py

import requests
import pytest

def test_server_response():
    """
    Test that the HTTP server is running on 127.0.0.1:8080,
    responds to GET /posterior with 200 OK, and returns the expected JSON.
    """
    url = "http://127.0.0.1:8080/posterior"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "mean_D" in data, "JSON response missing 'mean_D'"
    assert "std_D" in data, "JSON response missing 'std_D'"

    mean_d = data["mean_D"]
    std_d = data["std_D"]

    assert isinstance(mean_d, (int, float)), "'mean_D' must be a number"
    assert isinstance(std_d, (int, float)), "'std_D' must be a number"

    # The true diffusion coefficient is ~15.0. 
    # We allow a generous range to account for the specific random walk realization.
    assert 5.0 <= mean_d <= 25.0, f"mean_D {mean_d} is outside the expected reasonable range [5.0, 25.0]"
    assert std_d > 0, f"std_D {std_d} must be positive"