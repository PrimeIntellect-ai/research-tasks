# test_final_state.py

import os
import json
import pytest

def test_report_exists():
    report_path = "/home/user/archive_report.json"
    assert os.path.exists(report_path), f"The report file {report_path} was not found. Did the script run and generate it?"
    assert os.path.isfile(report_path), f"{report_path} is not a file."

def test_report_content_and_structure():
    report_path = "/home/user/archive_report.json"

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected_keys = {"valid_and_safe", "checksum_failed", "zip_slip_detected"}
    assert set(report_data.keys()) == expected_keys, f"The JSON report keys {set(report_data.keys())} do not match the expected keys {expected_keys}."

    expected_valid = ["alpha_data.tar.gz", "epsilon_data.zip"]
    expected_failed = ["gamma_data.tar.gz"]
    expected_slip = ["beta_data.zip", "delta_data.tar.gz"]

    assert report_data["valid_and_safe"] == expected_valid, (
        f"Expected 'valid_and_safe' to be {expected_valid}, but got {report_data['valid_and_safe']}. "
        "Ensure arrays are sorted alphabetically and files are correctly classified."
    )

    assert report_data["checksum_failed"] == expected_failed, (
        f"Expected 'checksum_failed' to be {expected_failed}, but got {report_data['checksum_failed']}. "
        "Ensure arrays are sorted alphabetically and files are correctly classified."
    )

    assert report_data["zip_slip_detected"] == expected_slip, (
        f"Expected 'zip_slip_detected' to be {expected_slip}, but got {report_data['zip_slip_detected']}. "
        "Ensure arrays are sorted alphabetically and files are correctly classified."
    )