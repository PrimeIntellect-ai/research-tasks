# test_final_state.py

import os
import csv
import json
import math
import pytest

def get_expected_results():
    data_path = "/home/user/sensor_data.csv"
    assert os.path.isfile(data_path), f"Input file {data_path} is missing."

    rows = []
    with open(data_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    # Impute humidity
    valid_h = [float(r["Humidity"]) for r in rows if r["Humidity"].strip() != ""]
    mean_h = sum(valid_h) / len(valid_h) if valid_h else 0.0

    cleaned_data = []
    for r in rows:
        h_str = r["Humidity"].strip()
        h_val = float(h_str) if h_str != "" else mean_h

        t_str = r["Temperature"].strip()
        p_str = r["Pressure"].strip()

        if t_str == "" or p_str == "":
            continue

        try:
            t_val = float(t_str)
            p_val = float(p_str)
        except ValueError:
            continue

        if t_val < -50.0 or t_val > 50.0:
            continue
        if p_val < 800.0 or p_val > 1200.0:
            continue

        cleaned_data.append({"t": t_val, "p": p_val, "h": h_val})

    n = len(cleaned_data)
    assert n > 0, "Cleaned dataset is empty, cannot compute statistics."

    # correlation
    sum_t = sum(d["t"] for d in cleaned_data)
    sum_p = sum(d["p"] for d in cleaned_data)
    sum_t2 = sum(d["t"]**2 for d in cleaned_data)
    sum_p2 = sum(d["p"]**2 for d in cleaned_data)
    sum_tp = sum(d["t"]*d["p"] for d in cleaned_data)

    numerator = n * sum_tp - sum_t * sum_p
    denominator = math.sqrt((n * sum_t2 - sum_t**2) * (n * sum_p2 - sum_p**2))
    correlation = numerator / denominator if denominator != 0 else 0.0

    # Bayesian Inference
    mu_0 = 20.0
    var_0 = 25.0
    var_pop = 16.0

    post_var = 1.0 / (1.0/var_0 + n/var_pop)
    post_mean = post_var * (mu_0/var_0 + sum_t/var_pop)

    return {
        "cleaned_row_count": n,
        "correlation_temp_pressure": correlation,
        "posterior_mean_temp": post_mean,
        "posterior_variance_temp": post_var
    }

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    with open(results_path, "r", encoding="utf-8") as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    expected = get_expected_results()

    assert "cleaned_row_count" in agent_data, "Missing 'cleaned_row_count' in results.json"
    assert "correlation_temp_pressure" in agent_data, "Missing 'correlation_temp_pressure' in results.json"
    assert "posterior_mean_temp" in agent_data, "Missing 'posterior_mean_temp' in results.json"
    assert "posterior_variance_temp" in agent_data, "Missing 'posterior_variance_temp' in results.json"

    assert int(agent_data["cleaned_row_count"]) == expected["cleaned_row_count"], \
        f"Expected cleaned_row_count {expected['cleaned_row_count']}, got {agent_data['cleaned_row_count']}"

    assert math.isclose(agent_data["correlation_temp_pressure"], expected["correlation_temp_pressure"], rel_tol=1e-3), \
        f"Expected correlation_temp_pressure {expected['correlation_temp_pressure']}, got {agent_data['correlation_temp_pressure']}"

    assert math.isclose(agent_data["posterior_mean_temp"], expected["posterior_mean_temp"], rel_tol=1e-3), \
        f"Expected posterior_mean_temp {expected['posterior_mean_temp']}, got {agent_data['posterior_mean_temp']}"

    assert math.isclose(agent_data["posterior_variance_temp"], expected["posterior_variance_temp"], rel_tol=1e-3), \
        f"Expected posterior_variance_temp {expected['posterior_variance_temp']}, got {agent_data['posterior_variance_temp']}"