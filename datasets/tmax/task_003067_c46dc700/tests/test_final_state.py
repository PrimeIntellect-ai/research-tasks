# test_final_state.py

import os
import json

def test_analyze_script_exists():
    script_path = '/home/user/analyze.py'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_report_exists_and_format():
    report_path = '/home/user/report.json'
    assert os.path.exists(report_path), f"Report file {report_path} does not exist. Did the script run successfully?"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not valid JSON."

    expected_keys = {"top_3_exp_ids", "bootstrap_mean", "ci_lower", "ci_upper"}
    actual_keys = set(report.keys())
    assert actual_keys == expected_keys, f"Report keys do not match. Expected {expected_keys}, got {actual_keys}"

    assert isinstance(report["top_3_exp_ids"], list), "top_3_exp_ids must be a list of strings."
    assert len(report["top_3_exp_ids"]) == 3, f"top_3_exp_ids must contain exactly 3 elements, got {len(report['top_3_exp_ids'])}."

    for val in ["bootstrap_mean", "ci_lower", "ci_upper"]:
        assert isinstance(report[val], (int, float)), f"{val} must be a number."

    assert report["ci_lower"] <= report["bootstrap_mean"], "ci_lower must be less than or equal to bootstrap_mean."
    assert report["bootstrap_mean"] <= report["ci_upper"], "bootstrap_mean must be less than or equal to ci_upper."

def test_report_values_plausible():
    report_path = '/home/user/report.json'
    if not os.path.exists(report_path):
        return # Handled by previous test

    with open(report_path, 'r') as f:
        report = json.load(f)

    # The metrics in the dataset are all between 0.69 and 0.89.
    # Therefore, the bootstrap mean and CIs must strictly fall within this range.
    assert 0.69 <= report["bootstrap_mean"] <= 0.89, f"bootstrap_mean {report['bootstrap_mean']} is out of plausible bounds based on the dataset."
    assert 0.69 <= report["ci_lower"] <= 0.89, f"ci_lower {report['ci_lower']} is out of plausible bounds."
    assert 0.69 <= report["ci_upper"] <= 0.89, f"ci_upper {report['ci_upper']} is out of plausible bounds."

    # The expected top 3 should be drawn from the available exp_ids
    valid_exp_ids = {"EXP_001", "EXP_002", "EXP_003", "EXP_004", "EXP_005", "EXP_006"}
    for exp_id in report["top_3_exp_ids"]:
        assert exp_id in valid_exp_ids, f"Invalid exp_id {exp_id} found in top_3_exp_ids."