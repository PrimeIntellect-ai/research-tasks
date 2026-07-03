# test_final_state.py
import json
import os
import pytest

def test_analysis_output_exists():
    assert os.path.isfile("/home/user/analysis_output.json"), "Output file /home/user/analysis_output.json is missing."

def test_analysis_output_structure():
    with open("/home/user/analysis_output.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file /home/user/analysis_output.json is not valid JSON.")

    assert "pagerank" in data, "Missing 'pagerank' key in output JSON."
    assert "shortest_paths_from_HUB_001" in data, "Missing 'shortest_paths_from_HUB_001' key in output JSON."

def test_pagerank_mse():
    with open("/home/user/analysis_output.json", "r") as f:
        agent_data = json.load(f).get("pagerank", {})
    with open("/opt/reference/analysis_output_golden.json", "r") as f:
        golden_data = json.load(f)["pagerank"]

    sq_errors = []
    for node_id, golden_val in golden_data.items():
        agent_val = agent_data.get(node_id, 0.0)
        sq_errors.append((golden_val - agent_val) ** 2)

    mse = sum(sq_errors) / len(sq_errors) if sq_errors else 1.0
    assert mse <= 1e-6, f"PageRank MSE is {mse}, which exceeds the threshold of 1e-6."

def test_shortest_paths():
    with open("/home/user/analysis_output.json", "r") as f:
        agent_data = json.load(f).get("shortest_paths_from_HUB_001", {})
    with open("/opt/reference/analysis_output_golden.json", "r") as f:
        golden_data = json.load(f)["shortest_paths_from_HUB_001"]

    for node_id, golden_val in golden_data.items():
        agent_val = agent_data.get(node_id)
        assert agent_val is not None, f"Missing shortest path for node {node_id}."
        assert abs(golden_val - agent_val) <= 1e-3, f"Shortest path for node {node_id} is {agent_val}, expected {golden_val}."