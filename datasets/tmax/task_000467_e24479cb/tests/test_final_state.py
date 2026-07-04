# test_final_state.py

import os
import h5py
import netCDF4 as nc
import numpy as np
from scipy.signal import butter, lfilter
from scipy.stats import gaussian_kde
from scipy.optimize import minimize
import requests
import pytest

def get_expected_cutoffs():
    ds = nc.Dataset('/app/trace_data.nc', 'r')
    telemetry = ds['telemetry'][:]
    reference = ds['reference'][:]
    ds.close()

    def normalize(arr):
        kde = gaussian_kde(arr)
        x = np.linspace(arr.min(), arr.max(), 1000)
        mode = x[np.argmax(kde(x))]
        std = np.std(arr)
        return (arr - mode) / std

    norm_tel = normalize(telemetry)
    norm_ref = normalize(reference)

    def objective(x):
        low, high = x
        if low >= high:
            return 1e9
        b, a = butter(4, [low, high], btype='bandpass', fs=1000)
        filt = lfilter(b, a, norm_tel)
        return np.mean((filt - norm_ref)**2)

    res = minimize(
        objective, 
        [40.0, 200.0], 
        bounds=[(10.0, 100.0), (150.0, 400.0)], 
        method='Nelder-Mead'
    )
    return res.x[0], res.x[1]

def test_hdf5_output():
    path = "/home/user/optimized_trace.h5"
    assert os.path.isfile(path), f"Output file {path} is missing."

    with h5py.File(path, 'r') as f:
        assert 'filtered_telemetry' in f, "Dataset 'filtered_telemetry' not found in HDF5 file."
        data = f['filtered_telemetry'][:]
        assert data.shape == (10000,), f"Expected shape (10000,), got {data.shape}."

def test_api_success():
    expected_low, expected_high = get_expected_cutoffs()

    url = "http://127.0.0.1:8080/api/v1/profile"
    try:
        resp = requests.post(url, json={"auth": "8142"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response is not valid JSON.")

    assert "low_cutoff" in data, "Missing 'low_cutoff' in response."
    assert "high_cutoff" in data, "Missing 'high_cutoff' in response."

    low = data["low_cutoff"]
    high = data["high_cutoff"]

    assert abs(low - expected_low) <= 0.5, f"low_cutoff {low} is not within 0.5 of expected {expected_low:.2f}"
    assert abs(high - expected_high) <= 0.5, f"high_cutoff {high} is not within 0.5 of expected {expected_high:.2f}"

def test_api_auth_failure():
    url = "http://127.0.0.1:8080/api/v1/profile"

    # Test wrong auth
    try:
        resp = requests.post(url, json={"auth": "0000"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")
    assert resp.status_code == 403, f"Expected HTTP 403 for invalid auth, got {resp.status_code}"

    # Test missing auth
    try:
        resp = requests.post(url, json={"wrong_key": "8142"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")
    assert resp.status_code == 403, f"Expected HTTP 403 for missing auth, got {resp.status_code}"