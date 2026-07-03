# test_final_state.py
import os
import re
import requests
import pytest

def test_trajectory_csv_exists_and_format():
    """Check that trajectory.csv exists and has the correct format and length."""
    csv_path = "/home/user/trajectory.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 1, f"{csv_path} is empty or missing data."
    assert lines[0].strip() == "frame,x,y", f"Header of {csv_path} is incorrect. Expected 'frame,x,y'."

    # The hidden ground truth says there are 300 frames.
    assert len(lines) == 301, f"Expected 300 frames (301 lines including header) in {csv_path}, got {len(lines)}."

def test_mcmc_sampler_cpp_exists():
    """Check that mcmc_sampler.cpp exists."""
    cpp_path = "/home/user/mcmc_sampler.cpp"
    assert os.path.exists(cpp_path), f"File {cpp_path} does not exist."

def test_parameters_txt_exists_and_values():
    """Check that parameters.txt exists and contains valid estimates."""
    param_path = "/home/user/parameters.txt"
    assert os.path.exists(param_path), f"File {param_path} does not exist."

    with open(param_path, 'r') as f:
        content = f.read()

    d_match = re.search(r'D=([0-9\.]+)', content)
    alpha_match = re.search(r'alpha=([0-9\.]+)', content)

    assert d_match is not None, f"Could not parse D from {param_path}."
    assert alpha_match is not None, f"Could not parse alpha from {param_path}."

    d_val = float(d_match.group(1))
    alpha_val = float(alpha_match.group(1))

    # Ground truth: D = 1.5, alpha = 0.75. Within 10%.
    assert 1.35 <= d_val <= 1.65, f"Estimated D ({d_val}) is not within 10% of true value 1.5."
    assert 0.675 <= alpha_val <= 0.825, f"Estimated alpha ({alpha_val}) is not within 10% of true value 0.75."

def test_simulation_service():
    """Check that the simulation service is running and returns correct JSON."""
    url = "http://localhost:8080/simulate?steps=50"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON.")

    assert "trajectory" in data, "JSON response must contain a 'trajectory' key."
    trajectory = data["trajectory"]

    assert isinstance(trajectory, list), "'trajectory' must be a list."
    assert len(trajectory) == 50, f"Expected 50 steps, got {len(trajectory)}."

    for i, point in enumerate(trajectory):
        assert "x" in point, f"Point at index {i} is missing 'x'."
        assert "y" in point, f"Point at index {i} is missing 'y'."
        assert isinstance(point["x"], (int, float)), f"'x' at index {i} must be a float."
        assert isinstance(point["y"], (int, float)), f"'y' at index {i} must be a float."