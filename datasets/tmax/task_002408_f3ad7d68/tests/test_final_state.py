# test_final_state.py
import os
import json
import csv
import pytest

def test_anomalies_json_exists():
    assert os.path.isfile('/home/user/anomalies.json'), "/home/user/anomalies.json does not exist."

def test_f1_score_and_structure():
    # Load agent output
    try:
        with open('/home/user/anomalies.json', 'r') as f:
            agent_data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read /home/user/anomalies.json: {e}")

    assert isinstance(agent_data, list), "/home/user/anomalies.json must be a JSON array."

    agent_ids = set()
    for item in agent_data:
        assert isinstance(item, dict), "Each item in anomalies.json must be a JSON object."
        for key in ["id", "timestamp", "ip_address", "response_time", "actor_group"]:
            assert key in item, f"Missing key '{key}' in output object: {item}"
        try:
            agent_ids.add(int(item['id']))
        except ValueError:
            pytest.fail(f"Invalid 'id' value in output: {item['id']}")

    # Calculate true anomalies based on ground truth logic
    # Rolling average of 5, threshold > 850
    try:
        with open('/home/user/server_logs.csv', 'r') as f:
            reader = list(csv.DictReader(f))
    except Exception as e:
        pytest.fail(f"Failed to read /home/user/server_logs.csv: {e}")

    true_ids = set()
    changepoint_hit = False
    for i in range(len(reader)):
        if not changepoint_hit and i >= 4:
            window = reader[i-4:i+1]
            avg = sum(int(r['response_time']) for r in window) / 5.0
            if avg > 850:
                changepoint_hit = True

        if changepoint_hit:
            true_ids.add(int(reader[i]['id']))

    # Compute F1 Score
    tp = len(agent_ids & true_ids)
    fp = len(agent_ids - true_ids)
    fn = len(true_ids - agent_ids)

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 Score is {f1:.4f}, which is below the threshold of 0.95. True anomalies count: {len(true_ids)}, Detected: {len(agent_ids)}"