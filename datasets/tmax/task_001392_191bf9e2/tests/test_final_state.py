# test_final_state.py

import os
import csv
import math
import glob
import pytest
import requests

def get_quantile(data, p):
    data = sorted(data)
    n = len(data)
    if n == 0:
        return None
    pos = (n - 1) * p
    i = int(math.floor(pos))
    f = pos - i
    if i + 1 < n:
        return data[i] + f * (data[i + 1] - data[i])
    else:
        return data[i]

def filter_outliers(group_data):
    if not group_data:
        return []
    q1 = get_quantile(group_data, 0.25)
    q3 = get_quantile(group_data, 0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    # Strictly less than or strictly greater than removed
    return [x for x in group_data if lower <= x <= upper]

def compute_stats(data):
    n = len(data)
    mean = sum(data) / n
    var = sum((x - mean) ** 2 for x in data) / (n - 1)
    return n, mean, var

def expected_results():
    data_a = []
    data_b = []

    for file in glob.glob('/home/user/data/raw/*.csv'):
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                val_str = row.get('value', '').strip()
                if not val_str or val_str.lower() == 'nan':
                    continue
                try:
                    val = float(val_str)
                    if row['group'] == 'A':
                        data_a.append(val)
                    elif row['group'] == 'B':
                        data_b.append(val)
                except ValueError:
                    pass

    clean_a = filter_outliers(data_a)
    clean_b = filter_outliers(data_b)

    n_a, mean_a, var_a = compute_stats(clean_a)
    n_b, mean_b, var_b = compute_stats(clean_b)

    t_stat = (mean_a - mean_b) / math.sqrt(var_a/n_a + var_b/n_b)

    return {
        "group_a_mean": mean_a,
        "group_b_mean": mean_b,
        "t_statistic": t_stat
    }

def test_server_response():
    url = "http://127.0.0.1:8080/api/stats"
    headers = {"Authorization": "Bearer token-stats-2024"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Server did not return valid JSON. Response: {response.text}")

    expected_keys = {
        "group_a_mean", "group_a_ci_lower", "group_a_ci_upper",
        "group_b_mean", "group_b_ci_lower", "group_b_ci_upper",
        "t_statistic", "p_value"
    }

    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"JSON response is missing keys: {missing_keys}"

    # Validate calculated values
    expected = expected_results()

    assert math.isclose(data["group_a_mean"], expected["group_a_mean"], rel_tol=1e-4, abs_tol=1e-4), \
        f"group_a_mean mismatch: expected {expected['group_a_mean']}, got {data['group_a_mean']}"

    assert math.isclose(data["group_b_mean"], expected["group_b_mean"], rel_tol=1e-4, abs_tol=1e-4), \
        f"group_b_mean mismatch: expected {expected['group_b_mean']}, got {data['group_b_mean']}"

    # Using abs(t_stat) because the order of subtraction might differ in student's implementation
    assert math.isclose(abs(data["t_statistic"]), abs(expected["t_statistic"]), rel_tol=1e-4, abs_tol=1e-4), \
        f"t_statistic mismatch: expected {expected['t_statistic']}, got {data['t_statistic']}"

    # Ensure CIs and p_value are numbers
    assert isinstance(data["p_value"], (int, float)), "p_value must be a number"
    assert isinstance(data["group_a_ci_lower"], (int, float)), "group_a_ci_lower must be a number"
    assert isinstance(data["group_a_ci_upper"], (int, float)), "group_a_ci_upper must be a number"

def test_makefile_fixed():
    makefile_path = "/app/statsserver/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "STATS_DATA_PATH=/home/user/data/processed/results.json" in content, \
        "Makefile does not correctly export STATS_DATA_PATH to the processed results.json."
    assert "port=8080" in content, "Makefile does not run the flask app on port 8080."