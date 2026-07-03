# test_final_state.py
import os
import json
import pytest

def test_report_exists():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The file {report_path} does not exist."

def test_report_content():
    report_path = "/home/user/report.json"
    truth_path = "/home/user/.truth.json"

    assert os.path.isfile(report_path), f"The file {report_path} does not exist."
    assert os.path.isfile(truth_path), f"The file {truth_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} is not a valid JSON file.")

    with open(truth_path, 'r') as f:
        truth_data = json.load(f)

    expected_keys = {"top_node_1", "top_node_1_c", "top_node_2", "top_node_2_c", "primer_lcs"}
    assert set(report_data.keys()) == expected_keys, f"report.json keys must be exactly {expected_keys}"

    assert report_data["top_node_1"] == truth_data["top_node_1"], "top_node_1 does not match the expected value."
    assert report_data["top_node_2"] == truth_data["top_node_2"], "top_node_2 does not match the expected value."

    assert report_data["top_node_1_c"] == pytest.approx(truth_data["top_node_1_c"], abs=1e-4), "top_node_1_c concentration does not match the expected value (rounded to 5 decimal places)."
    assert report_data["top_node_2_c"] == pytest.approx(truth_data["top_node_2_c"], abs=1e-4), "top_node_2_c concentration does not match the expected value (rounded to 5 decimal places)."

    assert report_data["primer_lcs"] == truth_data["primer_lcs"], "primer_lcs does not match the expected value."