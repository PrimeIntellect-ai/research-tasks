# test_final_state.py

import os
import json
import string
import pytest

def get_true_drifts():
    logs_path = "/app/agent_logs.jsonl"
    commits = []
    with open(logs_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("event_type") == "config_commit":
                    commits.append(data)
            except json.JSONDecodeError:
                continue

    commits.sort(key=lambda x: x["timestamp"])

    def normalize(payload):
        payload = payload.lower()
        to_remove = string.punctuation.replace('_', '')
        table = str.maketrans('', '', to_remove)
        payload = payload.translate(table)
        tokens = payload.split()
        return set(tokens)

    drifts = []
    prev_tokens = None
    for i, commit in enumerate(commits):
        tokens = normalize(commit["config_payload"])
        if i == 0:
            drift = 0.0
        else:
            intersection = len(tokens.intersection(prev_tokens))
            union = len(tokens.union(prev_tokens))
            jaccard = intersection / union if union > 0 else 1.0
            drift = 1.0 - jaccard
        drifts.append(drift)
        prev_tokens = tokens

    return drifts

def test_drift_report_mse():
    report_path = "/home/user/drift_report.json"
    assert os.path.exists(report_path), f"Agent report missing at {report_path}"

    with open(report_path, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Agent report at {report_path} is not valid JSON.")

    assert isinstance(agent_data, list), "Agent report must be a JSON list."

    true_drifts = get_true_drifts()

    assert len(agent_data) == len(true_drifts), f"Expected {len(true_drifts)} entries in report, but got {len(agent_data)}."

    mse = 0.0
    for i, (agent_entry, true_drift) in enumerate(zip(agent_data, true_drifts)):
        assert "drift_score" in agent_entry, f"Entry {i} missing 'drift_score' key."
        agent_drift = agent_entry["drift_score"]
        assert isinstance(agent_drift, (int, float)), f"Entry {i} 'drift_score' must be a number."
        mse += (agent_drift - true_drift) ** 2

    mse /= len(true_drifts)

    threshold = 0.005
    assert mse <= threshold, f"MSE of drift_score is {mse:.6f}, which exceeds the threshold of {threshold}."