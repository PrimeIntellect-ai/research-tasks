# test_final_state.py

import os
import json
import pytest

def test_rust_project_exists():
    assert os.path.isdir("/home/user/bio_analysis"), "The /home/user/bio_analysis directory is missing. You must create the Rust project there."
    assert os.path.isfile("/home/user/bio_analysis/Cargo.toml"), "The Cargo.toml file is missing in /home/user/bio_analysis. Ensure it is a valid Rust project."

def test_output_file_exists():
    assert os.path.isfile("/home/user/output/results.json"), "The output file /home/user/output/results.json is missing."

def test_results_match_truth():
    with open("/home/user/output/results.json", "r") as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/output/results.json is not valid JSON.")

    with open("/tmp/expected.json", "r") as f:
        truth_data = json.load(f)

    assert "peak_frequency" in agent_data, "Missing 'peak_frequency' in results.json"
    assert "largest_hydrophobic_cluster" in agent_data, "Missing 'largest_hydrophobic_cluster' in results.json"

    assert abs(agent_data["peak_frequency"] - truth_data["peak_frequency"]) < 0.002, \
        f"Expected peak_frequency to be approximately {truth_data['peak_frequency']}, got {agent_data['peak_frequency']}"

    assert agent_data["largest_hydrophobic_cluster"] == truth_data["largest_hydrophobic_cluster"], \
        f"Expected largest_hydrophobic_cluster to be {truth_data['largest_hydrophobic_cluster']}, got {agent_data['largest_hydrophobic_cluster']}"