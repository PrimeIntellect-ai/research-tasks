# test_final_state.py

import os
import json
import pytest

def test_report_json_exists():
    assert os.path.isfile("/home/user/report.json"), "The file /home/user/report.json does not exist."

def test_report_json_contents():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), "The file /home/user/report.json does not exist."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/report.json is not a valid JSON file.")

    expected_keys = {"total_valid_chains", "largest_chain_start_id", "largest_chain_size", "orphan_count"}
    actual_keys = set(report_data.keys())
    assert expected_keys.issubset(actual_keys), f"Missing keys in report.json. Expected: {expected_keys}, Found: {actual_keys}"

    assert report_data["total_valid_chains"] == 2, f"Expected total_valid_chains to be 2, got {report_data['total_valid_chains']}"
    assert report_data["largest_chain_start_id"] == "b4", f"Expected largest_chain_start_id to be 'b4', got '{report_data['largest_chain_start_id']}'"
    assert report_data["largest_chain_size"] == 210, f"Expected largest_chain_size to be 210, got {report_data['largest_chain_size']}"
    assert report_data["orphan_count"] == 3, f"Expected orphan_count to be 3, got {report_data['orphan_count']}"

def test_audit_go_exists():
    assert os.path.isfile("/home/user/audit.go"), "The file /home/user/audit.go does not exist. You must write the Go program."