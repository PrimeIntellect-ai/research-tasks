# test_final_state.py

import os
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

def test_tracking_endpoint():
    """Test that the /api/tracking endpoint returns the correct JSON structure."""
    url = f"{BASE_URL}/api/tracking"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /api/tracking is not valid JSON.")

    expected_keys = {"mean", "lower_bound", "upper_bound"}
    actual_keys = set(data.keys())

    assert expected_keys.issubset(actual_keys), f"JSON response is missing keys. Expected {expected_keys}, got {actual_keys}"

    # Check that they are numbers
    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"Expected {key} to be a number, got {type(data[key])}"

def test_plot_endpoint():
    """Test that the /api/plot endpoint returns a valid PNG image."""
    url = f"{BASE_URL}/api/plot"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Check PNG magic number
    magic_number = b'\x89PNG\r\n\x1a\n'
    assert response.content.startswith(magic_number), "The response does not appear to be a valid PNG image (magic number mismatch)."

def test_local_files_generated():
    """Test that the script actually generated the files in the expected locations."""
    json_path = "/home/user/tracking.json"
    plot_path = "/home/user/bootstrap_dist.png"

    assert os.path.exists(json_path), f"Expected tracking JSON file at {json_path} does not exist."
    assert os.path.exists(plot_path), f"Expected plot image file at {plot_path} does not exist."

    # Check that the plot is not empty (bug in initial script was saving an empty plot)
    # The empty plot might be very small, but let's just check it's > 0 bytes and is a PNG.
    size = os.path.getsize(plot_path)
    assert size > 1000, f"The plot file at {plot_path} seems suspiciously small ({size} bytes). Did you fix the plotting bug?"

    with open(plot_path, "rb") as f:
        header = f.read(8)
        assert header == b'\x89PNG\r\n\x1a\n', "The generated plot file is not a valid PNG."