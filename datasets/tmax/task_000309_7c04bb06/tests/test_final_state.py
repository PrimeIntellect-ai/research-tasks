# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"X-Research-Token": "sigma-99-alpha"}

def test_auth_required_stats():
    """Verify that the /stats endpoint requires authentication."""
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/stats: {e}")

    assert response.status_code in (401, 403), (
        f"Expected 401 or 403 when accessing /stats without auth, got {response.status_code}"
    )

def test_auth_required_plot():
    """Verify that the /plot endpoint requires authentication."""
    try:
        response = requests.get(f"{BASE_URL}/plot", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/plot: {e}")

    assert response.status_code in (401, 403), (
        f"Expected 401 or 403 when accessing /plot without auth, got {response.status_code}"
    )

def test_stats_endpoint():
    """Verify the /stats endpoint returns the correct JSON structure and values."""
    try:
        response = requests.get(f"{BASE_URL}/stats", headers=HEADERS, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/stats: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from /stats, got: {response.text}")

    expected_keys = {"t_stat", "p_value", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(data.keys())}"

    # Assert values are floats
    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"Expected {key} to be a number, got {type(data[key])}"

    # Check approximate values based on Welch's t-test
    # The prompt indicates expected t_stat is ~ 13.0673, p_value ~ 0.0058
    assert abs(data["t_stat"] - 13.0673) < 1.0, f"t_stat {data['t_stat']} is too far from expected ~13.0673"
    assert data["p_value"] < 0.05, f"p_value {data['p_value']} should be < 0.05"
    assert data["ci_lower"] > 0, "ci_lower should be positive (Treatment > Control)"
    assert data["ci_upper"] > data["ci_lower"], "ci_upper must be greater than ci_lower"

def test_plot_endpoint():
    """Verify the /plot endpoint returns a valid PNG image."""
    try:
        response = requests.get(f"{BASE_URL}/plot", headers=HEADERS, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/plot: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "image/png" in content_type.lower(), f"Expected Content-Type image/png, got {content_type}"

    # Check that the plot is not empty (which happens if the Template backend is used)
    content_length = len(response.content)
    assert content_length > 1000, f"Plot image is too small ({content_length} bytes). The matplotlib backend may not be fixed properly."

    # Check PNG magic bytes
    assert response.content.startswith(b"\x89PNG\r\n\x1a\n"), "Response content does not have valid PNG magic bytes."