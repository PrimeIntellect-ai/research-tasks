# test_final_state.py

import os
import json
import pytest
import numpy as np
import pandas as pd

def test_metrics_csv_exists():
    """Verify that the metrics.csv file was generated."""
    assert os.path.isfile("/home/user/metrics.csv"), "The /home/user/metrics.csv file is missing. Did you run the load test?"

def test_analysis_json_exists():
    """Verify that the analysis.json file was generated."""
    assert os.path.isfile("/home/user/analysis.json"), "The /home/user/analysis.json file is missing."

def test_analysis_metrics_accuracy():
    """Verify that the calculated metrics in analysis.json are accurate within the threshold."""
    # Ensure files exist before proceeding
    assert os.path.isfile("/home/user/metrics.csv"), "metrics.csv not found."
    assert os.path.isfile("/home/user/analysis.json"), "analysis.json not found."

    # Load the metrics data
    try:
        df = pd.read_csv('/home/user/metrics.csv')
    except Exception as e:
        pytest.fail(f"Failed to read /home/user/metrics.csv: {e}")

    required_columns = ['Time_s', 'Requests_Per_Sec', 'Latency_ms', 'CPU_util']
    for col in required_columns:
        assert col in df.columns, f"Missing required column '{col}' in metrics.csv"

    time = df['Time_s'].values
    req = df['Requests_Per_Sec'].values
    lat = df['Latency_ms'].values
    cpu = df['CPU_util'].values

    # Calculate expected values
    # 1. Integral of CPU over Time
    expected_integral = np.trapz(cpu, time)

    # 2. Max derivative of Latency over Time
    dt = np.diff(time)
    dlat = np.diff(lat)
    # Avoid division by zero if any dt == 0
    with np.errstate(divide='ignore', invalid='ignore'):
        derivs = dlat / dt
        expected_max_deriv = np.nanmax(derivs)

    # 3. Curve fitting (degree 2 polynomial)
    coeffs = np.polyfit(req, lat, 2)
    expected_a, expected_b, expected_c = coeffs[0], coeffs[1], coeffs[2]

    # Load agent's analysis data
    try:
        with open('/home/user/analysis.json', 'r') as f:
            agent_data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse /home/user/analysis.json: {e}")

    metrics_to_check = [
        ("total_cpu_integral", expected_integral),
        ("max_latency_derivative", expected_max_deriv),
        ("poly_a", expected_a),
        ("poly_b", expected_b),
        ("poly_c", expected_c)
    ]

    max_error = 0.0
    threshold = 0.01

    for key, expected_val in metrics_to_check:
        assert key in agent_data, f"Missing key '{key}' in analysis.json"

        agent_val = agent_data[key]
        assert isinstance(agent_val, (int, float)), f"Value for '{key}' must be a number, got {type(agent_val)}"

        err = abs(agent_val - expected_val)
        max_error = max(max_error, err)

        assert err <= threshold, (
            f"Mismatch for {key}. Expected ~{expected_val:.5f}, "
            f"Got {agent_val}. Absolute error: {err:.5f} (Threshold: <= {threshold})"
        )

    # Optional: Log the max error for visibility if tests pass
    print(f"All metrics within threshold. Maximum absolute error: {max_error:.5f}")