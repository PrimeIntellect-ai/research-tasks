# test_final_state.py
import urllib.request
import json
import numpy as np
import pytest

def get_expected_metrics():
    np.random.seed(42)
    true_peaks = []
    for _ in range(100):
        raw_signal = np.random.normal(50, 10, 100)
        # Apply 3-pt MA
        smoothed = np.convolve(raw_signal, np.ones(3)/3.0, mode='same')
        smoothed[0] = (raw_signal[0] + raw_signal[1]) / 2.0
        smoothed[-1] = (raw_signal[-2] + raw_signal[-1]) / 2.0
        true_peaks.append(np.max(smoothed))

    mean_val = np.mean(true_peaks)
    std_err = np.std(true_peaks) / np.sqrt(100)
    expected_lower = mean_val - 1.96 * std_err
    expected_upper = mean_val + 1.96 * std_err

    counts, _ = np.histogram(true_peaks, bins=5)
    expected_hist = counts.tolist()

    return expected_lower, expected_upper, expected_hist

def test_nginx_proxy_and_metrics():
    expected_lower, expected_upper, expected_hist = get_expected_metrics()

    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/api/data", timeout=5)
        body = req.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to fetch data from Nginx proxy at http://127.0.0.1:8080/api/data. Is Nginx configured correctly? Error: {e}")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Response from Nginx is not valid JSON: {body}")

    assert 'ci_lower' in data, "Missing 'ci_lower' in JSON response"
    assert 'ci_upper' in data, "Missing 'ci_upper' in JSON response"
    assert 'hist_counts' in data, "Missing 'hist_counts' in JSON response"

    ci_l = data['ci_lower']
    ci_u = data['ci_upper']
    hist = data['hist_counts']

    ci_lower_error = abs(ci_l - expected_lower)
    ci_upper_error = abs(ci_u - expected_upper)

    assert ci_lower_error <= 0.8, f"ci_lower error too high: expected ~{expected_lower:.2f}, got {ci_l} (absolute error: {ci_lower_error:.3f} > 0.8)"
    assert ci_upper_error <= 0.8, f"ci_upper error too high: expected ~{expected_upper:.2f}, got {ci_u} (absolute error: {ci_upper_error:.3f} > 0.8)"
    assert hist == expected_hist, f"Histogram mismatch: expected {expected_hist}, got {hist}"