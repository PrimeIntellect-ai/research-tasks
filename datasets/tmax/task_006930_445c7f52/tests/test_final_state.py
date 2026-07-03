# test_final_state.py

import os
import json
import subprocess
import hashlib
import csv

def test_regression_report_exists_and_valid():
    report_path = '/home/user/regression_report.json'
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not a valid JSON file."

    assert "ks_statistic" in report, "Missing 'ks_statistic' in regression_report.json"
    assert "p_value" in report, "Missing 'p_value' in regression_report.json"
    assert "is_deterministic" in report, "Missing 'is_deterministic' in regression_report.json"
    assert "reference_mean_z" in report, "Missing 'reference_mean_z' in regression_report.json"

    assert abs(report["ks_statistic"] - 0.0) < 1e-5, f"ks_statistic should be 0.0, got {report['ks_statistic']}"
    assert abs(report["p_value"] - 1.0) < 1e-5, f"p_value should be 1.0, got {report['p_value']}"
    assert report["is_deterministic"] is True, f"is_deterministic should be true, got {report['is_deterministic']}"

def test_reference_mean_z():
    ref_data_path = '/home/user/reference_data.csv'
    report_path = '/home/user/regression_report.json'

    assert os.path.isfile(ref_data_path), f"{ref_data_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, 'r') as f:
        report = json.load(f)

    z_values = []
    with open(ref_data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            z_values.append(float(row['z']))

    expected_mean = sum(z_values) / len(z_values)
    reported_mean = report["reference_mean_z"]

    assert abs(expected_mean - reported_mean) < 1e-5, f"reference_mean_z should be {expected_mean}, got {reported_mean}"

def get_file_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def test_lorenz_ensemble_is_deterministic():
    script_path = '/home/user/lorenz_ensemble.py'
    output_path = '/home/user/training_data.csv'

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # First run
    subprocess.run(["python3", script_path], check=True)
    assert os.path.isfile(output_path), f"Output {output_path} not generated after running script."
    hash1 = get_file_md5(output_path)

    # Second run
    subprocess.run(["python3", script_path], check=True)
    hash2 = get_file_md5(output_path)

    assert hash1 == hash2, "The output training_data.csv is not deterministic across multiple runs."