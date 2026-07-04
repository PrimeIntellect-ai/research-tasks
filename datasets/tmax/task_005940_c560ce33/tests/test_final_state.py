# test_final_state.py
import os
import json

def test_report_exists_and_correct():
    report_path = "/home/user/report.txt"
    truth_path = "/tmp/truth/bad_commit.txt"

    assert os.path.exists(report_path), f"{report_path} does not exist."
    assert os.path.exists(truth_path), f"Privileged truth file {truth_path} does not exist."

    with open(truth_path, "r") as f:
        expected_commit = f.read().strip()

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"{report_path} must contain exactly two lines."
    assert lines[0] == expected_commit, f"Line 1 of report.txt is incorrect. Expected the bad commit hash, got '{lines[0]}'."
    assert lines[1] == "data/edge_case_hang.log", f"Line 2 of report.txt is incorrect. Expected 'data/edge_case_hang.log', got '{lines[1]}'."

def test_output_json_correct():
    output_path = "/home/user/output.json"
    assert os.path.exists(output_path), f"{output_path} does not exist. Did you run the fixed script?"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{output_path} does not contain valid JSON."

    expected_data = ["start xx end", "hello"]
    assert data == expected_data, f"Output JSON is incorrect. Expected {expected_data}, got {data}."

def test_recovered_file_exists():
    recovered_path = "/home/user/log_processor/data/edge_case_hang.log"
    assert os.path.exists(recovered_path), f"Recovered test file {recovered_path} does not exist. Did you restore it from git history?"