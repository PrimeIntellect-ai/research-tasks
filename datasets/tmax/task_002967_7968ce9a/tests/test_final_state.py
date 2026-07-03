# test_final_state.py

import os
import pytest
import requests
import math

def test_plot_exists():
    """Test that the visualization plot exists."""
    plot_path = "/home/user/assay_fit.png"
    assert os.path.isfile(plot_path), f"Missing plot file: {plot_path}"

def test_kinetics_endpoint():
    """Test the /kinetics endpoint returns expected V_max and K_m."""
    try:
        response = requests.get("http://127.0.0.1:8000/kinetics", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /kinetics endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()

    assert "V_max" in data, "Missing V_max in /kinetics response"
    assert "K_m" in data, "Missing K_m in /kinetics response"

    # Check values are reasonably close to the setup script's truth
    assert math.isclose(data["V_max"], 200.0, rel_tol=0.1), f"V_max {data['V_max']} is not close to 200.0"
    assert math.isclose(data["K_m"], 15.0, rel_tol=0.2), f"K_m {data['K_m']} is not close to 15.0"

def test_distance_endpoint():
    """Test the /distance endpoint returns a wasserstein_distance."""
    try:
        response = requests.get("http://127.0.0.1:8000/distance", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /distance endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()

    assert "wasserstein_distance" in data, "Missing wasserstein_distance in /distance response"
    assert isinstance(data["wasserstein_distance"], (int, float)), "wasserstein_distance must be a number"
    assert data["wasserstein_distance"] > 0, "wasserstein_distance should be greater than 0"

def test_gc_content_endpoint():
    """Test the /gc_content endpoint returns the correct GC content percentages."""
    try:
        response = requests.get("http://127.0.0.1:8000/gc_content", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /gc_content endpoint: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()

    expected_gc = {
        "Seq1_promoter": 49.12,
        "Seq2_enhancer": 100.0,
        "Seq3_terminator": 0.0
    }

    for seq_id, expected_val in expected_gc.items():
        assert seq_id in data, f"Missing sequence ID {seq_id} in /gc_content response"
        assert math.isclose(data[seq_id], expected_val, abs_tol=0.05), \
            f"GC content for {seq_id} expected ~{expected_val}, got {data[seq_id]}"