# test_final_state.py
import math
import requests
import pytest

def get_expected_d1_d2(text: str):
    S = sum(ord(c) for c in text)
    floats = [(S * (i + 1)) % 100 / 100.0 for i in range(20)]
    d1 = sum(floats[:10]) / 10.0
    d2 = sum(floats[10:]) / 10.0
    return d1, d2

def get_stats(d1_list):
    n = len(d1_list)
    if n < 2:
        return 0.0, 0.0, 0.0
    mean = sum(d1_list) / n
    variance = sum((x - mean) ** 2 for x in d1_list) / (n - 1)
    std_dev = math.sqrt(variance)
    margin = 1.96 * std_dev / math.sqrt(n)
    return mean, mean - margin, mean + margin

def test_api_process_and_stats():
    base_url = "http://127.0.0.1:9000"

    words = ["hello", "world", "agent", "pytest", "golang"]
    d1_list = []

    for word in words:
        resp = requests.post(f"{base_url}/process", json={"text": word}, timeout=5)
        assert resp.status_code == 200, f"Expected status 200 for POST /process, got {resp.status_code}"

        data = resp.json()
        assert "reduced_vector" in data, "Response JSON missing 'reduced_vector' key"

        d1, d2 = data["reduced_vector"]
        exp_d1, exp_d2 = get_expected_d1_d2(word)

        assert math.isclose(d1, exp_d1, abs_tol=1e-3), f"For '{word}', expected D1 ~ {exp_d1}, got {d1}"
        assert math.isclose(d2, exp_d2, abs_tol=1e-3), f"For '{word}', expected D2 ~ {exp_d2}, got {d2}"

        d1_list.append(d1)

    # Now check stats
    resp = requests.get(f"{base_url}/stats", timeout=5)
    assert resp.status_code == 200, f"Expected status 200 for GET /stats, got {resp.status_code}"

    data = resp.json()
    assert "mean_d1" in data, "Response JSON missing 'mean_d1' key"
    assert "ci_lower" in data, "Response JSON missing 'ci_lower' key"
    assert "ci_upper" in data, "Response JSON missing 'ci_upper' key"

    exp_mean, exp_lower, exp_upper = get_stats(d1_list)

    assert math.isclose(data["mean_d1"], exp_mean, abs_tol=1e-3), f"Expected mean_d1 ~ {exp_mean}, got {data['mean_d1']}"
    assert math.isclose(data["ci_lower"], exp_lower, abs_tol=1e-3), f"Expected ci_lower ~ {exp_lower}, got {data['ci_lower']}"
    assert math.isclose(data["ci_upper"], exp_upper, abs_tol=1e-3), f"Expected ci_upper ~ {exp_upper}, got {data['ci_upper']}"