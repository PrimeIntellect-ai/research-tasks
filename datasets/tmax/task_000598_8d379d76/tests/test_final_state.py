# test_final_state.py

import pytest
import requests
import csv
import math
import os

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer pipe-auth-token-xyz"}
CSV_PATH = "/home/user/data/messy_logs.csv"

@pytest.fixture(scope="module")
def expected_data():
    assert os.path.exists(CSV_PATH), f"CSV file {CSV_PATH} is missing."

    records = []
    with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['CPU'] = float(row['CPU'])
            row['Memory'] = float(row['Memory'])
            records.append(row)

    # 1. Stats
    stats = {}
    for r in records:
        sid = r['ServerID']
        if sid not in stats:
            stats[sid] = {'cpu': [], 'mem': []}
        stats[sid]['cpu'].append(r['CPU'])
        stats[sid]['mem'].append(r['Memory'])

    expected_stats = {}
    for sid, vals in stats.items():
        expected_stats[sid] = {
            "avg_cpu": sum(vals['cpu']) / len(vals['cpu']),
            "max_mem": float(max(vals['mem']))
        }

    # 2. Distance
    alpha_cpu = [r['CPU'] for r in sorted(records, key=lambda x: x['Timestamp']) if r['ServerID'] == 'Server-Alpha']
    beta_cpu = [r['CPU'] for r in sorted(records, key=lambda x: x['Timestamp']) if r['ServerID'] == 'Server-Beta']

    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(alpha_cpu, beta_cpu)))

    # 3. Sample
    levels = {}
    for r in sorted(records, key=lambda x: x['Timestamp']):
        lvl = r['LogLevel']
        if lvl not in levels:
            levels[lvl] = []
        if len(levels[lvl]) < 2:
            levels[lvl].append(r)

    expected_sample = []
    for lvl in sorted(levels.keys()):
        expected_sample.extend(levels[lvl])

    return expected_stats, dist, expected_sample

def test_auth_required():
    """Verify that endpoints require the correct Authorization header."""
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not reachable at 127.0.0.1:8080.")

    assert response.status_code in (401, 403), f"Expected 401/403 when missing auth header, got {response.status_code}"

def test_stats_endpoint(expected_data):
    """Verify the /stats endpoint returns correct summary statistics."""
    expected_stats, _, _ = expected_data

    response = requests.get(f"{BASE_URL}/stats", headers=AUTH_HEADER, timeout=5)
    assert response.status_code == 200, f"/stats returned status {response.status_code}. Body: {response.text}"

    data = response.json()
    assert isinstance(data, dict), "Expected a JSON dictionary from /stats"

    for server_id, expected_vals in expected_stats.items():
        assert server_id in data, f"Missing {server_id} in /stats response"
        assert math.isclose(data[server_id]["avg_cpu"], expected_vals["avg_cpu"], rel_tol=1e-5), \
            f"Incorrect avg_cpu for {server_id}. Expected {expected_vals['avg_cpu']}, got {data[server_id]['avg_cpu']}"
        assert math.isclose(data[server_id]["max_mem"], expected_vals["max_mem"], rel_tol=1e-5), \
            f"Incorrect max_mem for {server_id}. Expected {expected_vals['max_mem']}, got {data[server_id]['max_mem']}"

def test_distance_endpoint(expected_data):
    """Verify the /distance endpoint returns the correct Euclidean distance."""
    _, expected_dist, _ = expected_data

    response = requests.get(f"{BASE_URL}/distance", headers=AUTH_HEADER, timeout=5)
    assert response.status_code == 200, f"/distance returned status {response.status_code}. Body: {response.text}"

    data = response.json()
    assert "euclidean_distance" in data, "Missing 'euclidean_distance' key in /distance response"

    actual_dist = data["euclidean_distance"]
    assert math.isclose(actual_dist, expected_dist, rel_tol=1e-5), \
        f"Incorrect euclidean_distance. Expected {expected_dist}, got {actual_dist}"

def test_sample_endpoint(expected_data):
    """Verify the /sample endpoint returns the correct stratified sample."""
    _, _, expected_sample = expected_data

    response = requests.get(f"{BASE_URL}/sample", headers=AUTH_HEADER, timeout=5)
    assert response.status_code == 200, f"/sample returned status {response.status_code}. Body: {response.text}"

    data = response.json()
    assert isinstance(data, list), "Expected a JSON list from /sample"
    assert len(data) == len(expected_sample), f"Expected {len(expected_sample)} records in sample, got {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_sample)):
        assert actual["LogLevel"] == expected["LogLevel"], f"Record {i}: Expected LogLevel {expected['LogLevel']}, got {actual.get('LogLevel')}"
        assert actual["Timestamp"] == expected["Timestamp"], f"Record {i}: Expected Timestamp {expected['Timestamp']}, got {actual.get('Timestamp')}"
        assert actual["ServerID"] == expected["ServerID"], f"Record {i}: Expected ServerID {expected['ServerID']}, got {actual.get('ServerID')}"
        assert math.isclose(float(actual["CPU"]), expected["CPU"], rel_tol=1e-5), f"Record {i}: CPU mismatch"
        assert math.isclose(float(actual["Memory"]), expected["Memory"], rel_tol=1e-5), f"Record {i}: Memory mismatch"
        assert actual["Message"] == expected["Message"], f"Record {i}: Expected Message {repr(expected['Message'])}, got {repr(actual.get('Message'))}"