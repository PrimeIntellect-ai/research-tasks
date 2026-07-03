# test_final_state.py
import os
import json
import pytest

def test_results_json_exists():
    assert os.path.isfile("/home/user/results.json"), "The file /home/user/results.json does not exist."

def test_results_json_content():
    with open("/home/user/results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/results.json is not a valid JSON file.")

    expected_sensors = ["sensor1.fits", "sensor2.fits", "sensor3.fits", "sensor4.fits"]
    for sensor in expected_sensors:
        assert sensor in data, f"Key '{sensor}' is missing from results.json."

        sensor_data = data[sensor]
        assert "calibrated_freq" in sensor_data, f"'calibrated_freq' missing in {sensor}."
        assert "mean_magnitude" in sensor_data, f"'mean_magnitude' missing in {sensor}."

    # Expected values
    expected_calibrated_freq = {
        "sensor1.fits": 6.285714285714286,
        "sensor2.fits": 17.714285714285715,
        "sensor3.fits": 32.0,
        "sensor4.fits": 60.57142857142857
    }

    expected_mean_magnitude = {
        "sensor1.fits": 15.65,
        "sensor2.fits": 15.42,
        "sensor3.fits": 15.61,
        "sensor4.fits": 15.53
    }

    for sensor in expected_sensors:
        calib_freq = data[sensor]["calibrated_freq"]
        mean_mag = data[sensor]["mean_magnitude"]

        assert isinstance(calib_freq, (int, float)), f"'calibrated_freq' for {sensor} must be a number."
        assert isinstance(mean_mag, (int, float)), f"'mean_magnitude' for {sensor} must be a number."

        assert abs(calib_freq - expected_calibrated_freq[sensor]) < 0.01, \
            f"Incorrect 'calibrated_freq' for {sensor}. Expected ~{expected_calibrated_freq[sensor]:.4f}, got {calib_freq}."

        assert abs(mean_mag - expected_mean_magnitude[sensor]) / expected_mean_magnitude[sensor] < 0.05, \
            f"Incorrect 'mean_magnitude' for {sensor}. Expected ~{expected_mean_magnitude[sensor]:.2f}, got {mean_mag}."

def test_go_source_exists():
    assert os.path.isfile("/home/user/analyze.go"), "The Go source file /home/user/analyze.go does not exist."

def test_go_module_initialized():
    assert os.path.isfile("/home/user/go.mod"), "Go module not initialized (/home/user/go.mod is missing)."