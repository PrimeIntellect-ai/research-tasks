# test_final_state.py

import os
import json
import pytest

def test_cpp_file_exists():
    cpp_path = "/home/user/workspace/verify_backup.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."

def test_report_json_exists_and_valid():
    report_path = "/home/user/workspace/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "highest_out_degree_node" in data, "Key 'highest_out_degree_node' missing from report.json."
    assert "pattern_match_count" in data, "Key 'pattern_match_count' missing from report.json."

    assert data["highest_out_degree_node"] == 1, f"Expected highest_out_degree_node to be 1, got {data['highest_out_degree_node']}."
    assert data["pattern_match_count"] == 3, f"Expected pattern_match_count to be 3, got {data['pattern_match_count']}."