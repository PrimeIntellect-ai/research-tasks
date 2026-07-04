# test_final_state.py
import os
import json
import math
import time
import requests
import numpy as np
import scipy.io.wavfile as wavfile

def kahan_sum(values):
    s = 0.0
    c = 0.0
    for v in values:
        y = v - c
        t = s + y
        c = (t - s) - y
        s = t
    return s

def compute_expected_energy():
    sample_rate, data = wavfile.read('/app/stress_test.wav')
    data = data.astype(np.float64)
    total_segments = 4
    segment_index = 1
    N = len(data)
    segment_length = int(math.floor(N / total_segments))

    start = segment_index * segment_length
    segment = data[start:start+segment_length]

    n = np.arange(segment_length)
    window = 0.5 * (1.0 - np.cos(2.0 * np.pi * n / (segment_length - 1)))
    windowed = segment * window

    fft_res = np.fft.fft(windowed)
    energy = np.real(fft_res)**2 + np.imag(fft_res)**2

    start_freq = 1000.0
    end_freq = 2000.0

    freqs = np.arange(segment_length) * sample_rate / segment_length
    mask = (freqs >= start_freq) & (freqs <= end_freq)

    filtered_energy = energy[mask]
    return kahan_sum(filtered_energy)

def test_service_ready_file():
    ready_file = "/home/user/service_ready.txt"
    assert os.path.isfile(ready_file), f"Service ready file not found at {ready_file}"
    with open(ready_file, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"Expected ready file to contain 'READY', got '{content}'"

def test_analyze_endpoint():
    # Allow a brief moment for the service to actually be listening if it just wrote the file
    time.sleep(1)

    url = "http://127.0.0.1:8080/analyze"
    payload = {
        "segment_index": 1,
        "total_segments": 4,
        "start_freq": 1000.0,
        "end_freq": 2000.0,
        "reference_val": 50000000000.0
    }

    try:
        resp = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        raise AssertionError(f"Failed to connect to the service at {url}: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise AssertionError(f"Failed to parse response as JSON. Response: {resp.text}")

    assert "energy" in data, f"Response JSON missing 'energy' field: {data}"
    assert "difference" in data, f"Response JSON missing 'difference' field: {data}"

    actual_energy = float(data["energy"])
    actual_difference = float(data["difference"])

    expected_energy = compute_expected_energy()
    expected_difference = abs(expected_energy - 50000000000.0)

    # Allow a small relative tolerance due to potential minor differences between rustfft and numpy.fft
    rel_tol = 1e-4

    energy_diff = abs(actual_energy - expected_energy)
    assert energy_diff <= rel_tol * expected_energy, \
        f"Energy mismatch. Expected ~{expected_energy}, got {actual_energy}"

    diff_diff = abs(actual_difference - expected_difference)
    assert diff_diff <= rel_tol * expected_difference, \
        f"Difference mismatch. Expected ~{expected_difference}, got {actual_difference}"