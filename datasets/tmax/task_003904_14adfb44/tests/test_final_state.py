# test_final_state.py
import os
import requests
import pytest
import math

def test_spectrum_plot_exists():
    path = "/home/user/spectrum.png"
    assert os.path.isfile(path), f"The spectrum plot {path} does not exist."

def test_frequency_endpoint():
    try:
        response = requests.get("http://127.0.0.1:8080/frequency", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API for /frequency: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /frequency is not valid JSON.")

    assert "video_dominant_hz" in data, "Response JSON missing 'video_dominant_hz' key."

    freq = data["video_dominant_hz"]
    assert isinstance(freq, (int, float)), "Frequency must be a number."
    assert math.isclose(freq, 4.5, abs_tol=0.2), f"Expected frequency around 4.5 Hz, got {freq}"

def test_simulate_endpoint_reproducibility():
    try:
        response1 = requests.post("http://127.0.0.1:8080/simulate", timeout=30)
        response2 = requests.post("http://127.0.0.1:8080/simulate", timeout=30)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API for /simulate: {e}")

    assert response1.status_code == 200, f"Expected HTTP 200 on first POST, got {response1.status_code}"
    assert response2.status_code == 200, f"Expected HTTP 200 on second POST, got {response2.status_code}"

    try:
        data1 = response1.json()
        data2 = response2.json()
    except ValueError:
        pytest.fail("Response from /simulate is not valid JSON.")

    assert "energy" in data1, "First response JSON missing 'energy' key."
    assert "energy" in data2, "Second response JSON missing 'energy' key."

    energy1 = data1["energy"]
    energy2 = data2["energy"]

    assert isinstance(energy1, (float, int)), "Energy must be a number."
    assert isinstance(energy2, (float, int)), "Energy must be a number."

    assert energy1 == energy2, f"Energy results are not exactly equal bit-for-bit: {energy1} != {energy2}. The reduction order issue was not properly fixed."