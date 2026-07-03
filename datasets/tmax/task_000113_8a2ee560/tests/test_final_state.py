# test_final_state.py
import os
import requests
import pytest
import time

def test_trajectory_csv_exists():
    """Verify that the trajectory.csv file was generated."""
    csv_path = "/home/user/trajectory.csv"
    assert os.path.exists(csv_path), f"Expected trajectory file at {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"Path {csv_path} is not a file."
    assert os.path.getsize(csv_path) > 0, f"Trajectory file {csv_path} is empty."

def test_api_response():
    """Verify the API response from the background service."""
    url = "http://127.0.0.1:9090/analysis"

    # Retry logic in case the server takes a moment to start
    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(1)

    assert response is not None, f"Failed to connect to the service at {url}"
    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

    expected_keys = {"acceleration_m_s2", "linear_rss", "quadratic_rss", "integrated_displacement_m"}
    assert expected_keys.issubset(data.keys()), f"JSON response is missing required keys. Expected: {expected_keys}, Got: {set(data.keys())}"

    accel = data["acceleration_m_s2"]
    lin_rss = data["linear_rss"]
    quad_rss = data["quadratic_rss"]
    disp = data["integrated_displacement_m"]

    assert isinstance(accel, (int, float)), "acceleration_m_s2 must be a number"
    assert isinstance(lin_rss, (int, float)), "linear_rss must be a number"
    assert isinstance(quad_rss, (int, float)), "quadratic_rss must be a number"
    assert isinstance(disp, (int, float)), "integrated_displacement_m must be a number"

    assert abs(accel - 9.81) < 0.5, f"Expected acceleration ~9.81 m/s^2, got {accel}"
    assert lin_rss > 1000, f"Expected linear_rss to be very high (>1000), got {lin_rss}"
    assert quad_rss < 50, f"Expected quadratic_rss to be low (<50), got {quad_rss}"
    assert abs(disp - 3.75) < 0.5, f"Expected integrated displacement ~3.75 m, got {disp}"