# test_final_state.py

import os
import ast
import pytest
import requests
import numpy as np
from scipy.stats import gaussian_kde

def test_test_api_script_exists_and_valid():
    script_path = "/home/user/test_api.py"
    assert os.path.isfile(script_path), f"Test script is missing at {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"Test script {script_path} contains invalid Python syntax: {e}")

def test_plot_data_script_exists_and_valid():
    script_path = "/home/user/plot_data.py"
    assert os.path.isfile(script_path), f"Plot script is missing at {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"Plot script {script_path} contains invalid Python syntax: {e}")

def test_experiment_viz_exists():
    image_path = "/home/user/experiment_viz.png"
    assert os.path.isfile(image_path), f"Visualization image is missing at {image_path}"

def test_audio_peaks_endpoint():
    url = "http://127.0.0.1:8080/audio_peaks"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON")

    assert "peaks" in data, "JSON response missing 'peaks' key"
    peaks = data["peaks"]
    assert isinstance(peaks, list), "'peaks' should be a list"
    assert len(peaks) == 3, f"Expected 3 peaks, got {len(peaks)}"

    expected_peaks = [300, 600, 900]
    for actual, expected in zip(sorted(peaks), expected_peaks):
        assert abs(actual - expected) <= 5, f"Peak {actual} is not within 5 Hz of expected {expected}"

def test_mesh_density_endpoint():
    csv_path = "/home/user/samples.csv"
    assert os.path.isfile(csv_path), f"Samples CSV is missing at {csv_path}"

    samples = np.loadtxt(csv_path)
    kde = gaussian_kde(samples, bw_method='scott')
    eval_points = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
    expected_density = kde(eval_points)

    url = "http://127.0.0.1:8080/mesh_density"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON")

    assert "density" in data, "JSON response missing 'density' key"
    density = data["density"]
    assert isinstance(density, list), "'density' should be a list"
    assert len(density) == 9, f"Expected 9 density values, got {len(density)}"

    np.testing.assert_allclose(density, expected_density, rtol=1e-3, atol=1e-4, err_msg="Density values do not match expected KDE evaluation")