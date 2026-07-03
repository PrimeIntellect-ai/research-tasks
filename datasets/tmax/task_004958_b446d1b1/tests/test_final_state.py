# test_final_state.py
import csv
import math
import statistics
import requests
import pytest

def get_expected_values():
    valid_values = []
    raw_data = []
    with open('/home/user/sensor_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            val_str = row['value'].strip()
            raw_data.append(val_str)
            if val_str and val_str != "NaN":
                try:
                    valid_values.append(float(val_str))
                except ValueError:
                    pass

    median_val = statistics.median(valid_values)

    cleaned_data = []
    for val_str in raw_data:
        if val_str == "" or val_str == "NaN":
            val = median_val
        else:
            val = float(val_str)

        if 0.0 <= val <= 100.0:
            cleaned_data.append(val)

    n = len(cleaned_data)
    sample_variance = statistics.variance(cleaned_data)

    prior_mean = 50.0
    prior_var = 25.0

    sum_x = sum(cleaned_data)

    post_var = 1.0 / (1.0 / prior_var + n / sample_variance)
    post_mean = post_var * (prior_mean / prior_var + sum_x / sample_variance)

    return n, sample_variance, post_mean, post_var

def test_api_stats():
    expected_n, expected_var, _, _ = get_expected_values()

    try:
        resp = requests.get('http://127.0.0.1:8123/stats', timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /stats endpoint: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"

    data = resp.json()
    assert 'clean_count' in data, "Missing 'clean_count' in /stats response"
    assert 'sample_variance' in data, "Missing 'sample_variance' in /stats response"

    assert data['clean_count'] == expected_n, f"Expected clean_count {expected_n}, got {data['clean_count']}"
    assert math.isclose(data['sample_variance'], expected_var, rel_tol=1e-4), \
        f"Expected sample_variance {expected_var}, got {data['sample_variance']}"

def test_api_posterior():
    _, _, expected_post_mean, expected_post_var = get_expected_values()

    try:
        resp = requests.get('http://127.0.0.1:8123/posterior', timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /posterior endpoint: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"

    data = resp.json()
    assert 'posterior_mean' in data, "Missing 'posterior_mean' in /posterior response"
    assert 'posterior_variance' in data, "Missing 'posterior_variance' in /posterior response"

    assert math.isclose(data['posterior_mean'], expected_post_mean, rel_tol=1e-4), \
        f"Expected posterior_mean {expected_post_mean}, got {data['posterior_mean']}"
    assert math.isclose(data['posterior_variance'], expected_post_var, rel_tol=1e-4), \
        f"Expected posterior_variance {expected_post_var}, got {data['posterior_variance']}"