# test_final_state.py
import json
import os
import pytest

def test_report_jaccard_similarity():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    try:
        with open(report_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {report_path} is not valid JSON.")

    assert "outdated_components" in data, "Key 'outdated_components' is missing from report.json."

    agent_list = data.get("outdated_components", [])
    assert isinstance(agent_list, list), "'outdated_components' must be a list."

    agent_data = set(agent_list)
    truth_data = {"auth-service", "frontend"}

    intersection = len(agent_data.intersection(truth_data))
    union = len(agent_data.union(truth_data))
    jaccard = intersection / union if union > 0 else 0.0

    assert jaccard >= 0.95, f"Jaccard similarity {jaccard:.2f} is below threshold 0.95. Agent components: {agent_data}, Expected: {truth_data}"