# test_final_state.py
import os
import math
import requests
import pytest

def compute_peak_B(seq):
    k1 = seq.count('A') * 0.1 + 0.05
    k2 = (seq.count('B') + seq.count('C')) * 0.05 + 0.02
    A0 = 100.0

    max_B = 0.0
    for i in range(1000):
        t = 50.0 * i / 999.0
        if abs(k1 - k2) < 1e-9:
            B = k1 * A0 * t * math.exp(-k1 * t)
        else:
            B = k1 * A0 / (k2 - k1) * (math.exp(-k1 * t) - math.exp(-k2 * t))
        if B > max_B:
            max_B = B
    return max_B

def get_expected_results(sequences):
    results = []
    for seq in sequences:
        results.append({
            'sequence': seq,
            'length': len(seq),
            'peak_B': compute_peak_B(seq)
        })

    results.sort(key=lambda x: x['sequence'])

    total_peak = 0.0
    for r in results:
        total_peak += r['peak_B']

    n = len(results)
    sum_x = sum(r['length'] for r in results)
    sum_y = sum(r['peak_B'] for r in results)
    sum_x2 = sum(r['length']**2 for r in results)
    sum_xy = sum(r['length'] * r['peak_B'] for r in results)

    denominator = n * sum_x2 - sum_x**2
    if denominator == 0:
        slope = 0.0
        intercept = sum_y / n if n else 0.0
    else:
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n

    return total_peak, slope, intercept

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/simulate"
    payload = {"sequences": ["A"]}
    try:
        response = requests.post(url, json=payload, timeout=5)
        assert response.status_code in [401, 403], f"Expected 401 or 403 for unauthorized request, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

def test_api_authorized_and_correctness():
    url = "http://127.0.0.1:8080/simulate"
    headers = {"Authorization": "Bearer bio-secret-2024"}
    sequences = ["A", "AB", "ABC", "BCA", "AABBCC", "AAABBBCCC", "ACACAC"]
    payload = {"sequences": sequences}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

        data = response.json()
        assert "total_peak" in data, "Missing total_peak in response"
        assert "regression_slope" in data, "Missing regression_slope in response"
        assert "regression_intercept" in data, "Missing regression_intercept in response"

        expected_total, expected_slope, expected_intercept = get_expected_results(sequences)

        assert math.isclose(data["total_peak"], expected_total, rel_tol=1e-2), \
            f"total_peak mismatch. Expected ~{expected_total}, got {data['total_peak']}"
        assert math.isclose(data["regression_slope"], expected_slope, rel_tol=1e-2), \
            f"regression_slope mismatch. Expected ~{expected_slope}, got {data['regression_slope']}"
        assert math.isclose(data["regression_intercept"], expected_intercept, rel_tol=1e-2), \
            f"regression_intercept mismatch. Expected ~{expected_intercept}, got {data['regression_intercept']}"

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API or request timed out: {e}")

def test_plot_generated():
    assert os.path.isfile("/home/user/plot.png"), "Plot file /home/user/plot.png was not generated"
    assert os.path.getsize("/home/user/plot.png") > 0, "Plot file /home/user/plot.png is empty"