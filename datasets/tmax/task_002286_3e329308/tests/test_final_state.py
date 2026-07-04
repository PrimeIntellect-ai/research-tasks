# test_final_state.py

import os
import json
import time
import subprocess
import pandas as pd
import pytest

def test_result_json_correctness():
    """
    Validates that the output JSON exists and contains the correctly aggregated
    data for customer '88472' by recomputing the truth from the CSV files.
    """
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Result JSON file is missing at {result_path}"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} does not contain valid JSON.")

    assert "customer_id" in data, "Missing 'customer_id' key in JSON output"
    assert str(data["customer_id"]) == "88472", f"Incorrect customer_id: expected '88472', got {data['customer_id']}"
    assert "departments" in data, "Missing 'departments' key in JSON output"

    # Recompute ground truth using pandas
    tickets_path = "/app/data/tickets.csv"
    agents_path = "/app/data/agents.csv"

    assert os.path.isfile(tickets_path), f"Missing {tickets_path}"
    assert os.path.isfile(agents_path), f"Missing {agents_path}"

    tickets = pd.read_csv(tickets_path)
    agents = pd.read_csv(agents_path)

    # Ensure string comparison for customer_id
    tickets['customer_id'] = tickets['customer_id'].astype(str)
    customer_tickets = tickets[tickets['customer_id'] == "88472"]

    merged = pd.merge(customer_tickets, agents, on='agent_id')
    expected_departments = {}
    for dept, group in merged.groupby('department'):
        expected_departments[dept] = {
            "total_duration": int(group['duration_mins'].sum()),
            "avg_rating": float(group['rating'].mean())
        }

    agent_depts = data["departments"]

    # Check if all expected departments are present
    assert set(agent_depts.keys()) == set(expected_departments.keys()), \
        f"Department keys mismatch. Expected: {list(expected_departments.keys())}, Got: {list(agent_depts.keys())}"

    for dept in expected_departments:
        expected_dur = expected_departments[dept]["total_duration"]
        expected_rat = expected_departments[dept]["avg_rating"]

        assert "total_duration" in agent_depts[dept], f"Missing 'total_duration' for department {dept}"
        assert "avg_rating" in agent_depts[dept], f"Missing 'avg_rating' for department {dept}"

        agent_dur = agent_depts[dept]["total_duration"]
        agent_rat = agent_depts[dept]["avg_rating"]

        assert abs(agent_dur - expected_dur) < 1e-5, \
            f"Total duration mismatch for {dept}. Expected {expected_dur}, got {agent_dur}"
        assert abs(agent_rat - expected_rat) < 1e-2, \
            f"Average rating mismatch for {dept}. Expected {expected_rat:.2f}, got {agent_rat:.2f}"

def test_speedup_metric():
    """
    Measures the execution time of the optimized analyzer against the naive baseline.
    Asserts that the speedup is at least 10.0x.
    """
    analyzer_path = "/home/user/analyzer"
    naive_path = "/opt/baseline/analyze_naive"
    customer_id = "88472"

    assert os.path.isfile(analyzer_path), f"Optimized binary missing at {analyzer_path}. Did you compile it?"
    assert os.path.isfile(naive_path), f"Baseline naive binary missing at {naive_path}"

    # Measure Optimized Time
    start_opt = time.time()
    try:
        subprocess.run([analyzer_path, customer_id], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Optimized binary failed to execute: {e.stderr.decode('utf-8', errors='ignore')}")
    t_opt = time.time() - start_opt

    # Measure Naive Time
    start_naive = time.time()
    try:
        subprocess.run([naive_path, customer_id], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Baseline naive binary failed to execute: {e.stderr.decode('utf-8', errors='ignore')}")
    t_naive = time.time() - start_naive

    # Prevent division by zero if execution is implausibly fast
    t_opt = max(t_opt, 1e-6)

    speedup = t_naive / t_opt

    assert speedup >= 10.0, f"Speedup metric failed: achieved {speedup:.2f}x (Threshold >= 10.0x). Naive: {t_naive:.4f}s, Optimized: {t_opt:.4f}s"