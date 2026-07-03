# test_final_state.py

import os
import json
import subprocess
import pytest

def test_login_service_executable_exists_and_permissions():
    exe_path = "/home/user/login_service"
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist. Did you compile the C program?"
    assert os.path.isfile(exe_path), f"Path {exe_path} is not a file."
    assert os.access(exe_path, os.X_OK), f"Executable {exe_path} does not have execute permissions."

def test_login_service_behavior():
    exe_path = "/home/user/login_service"

    test_cases = [
        ("/secure/dashboard", "Location: /secure/dashboard\r\n\r\n"),
        ("http://evil.com", "Location: /secure/default\r\n\r\n"),
        ("//evil.com", "Location: /secure/default\r\n\r\n"),
        ("/secure//test", "Location: /secure/default\r\n\r\n"),
        ("secure/dashboard", "Location: /secure/default\r\n\r\n"),
        ("/secure/", "Location: /secure/\r\n\r\n")
    ]

    for arg, expected_output in test_cases:
        result = subprocess.run([exe_path, arg], capture_output=True, text=True)
        actual_output = result.stdout
        assert actual_output == expected_output, (
            f"Running '{exe_path} {arg}' produced incorrect output.\n"
            f"Expected: {repr(expected_output)}\n"
            f"Got: {repr(actual_output)}"
        )

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    assert os.path.isfile(report_path), f"Path {report_path} is not a file."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"File {report_path} is not valid JSON: {e}")

    assert "malicious_ips" in report_data, "The 'malicious_ips' key is missing from the JSON report."
    assert "issuer_org" in report_data, "The 'issuer_org' key is missing from the JSON report."

    expected_ips = ["10.0.0.5", "172.16.0.4"]
    actual_ips = report_data["malicious_ips"]
    assert actual_ips == expected_ips, (
        f"The 'malicious_ips' array is incorrect.\n"
        f"Expected: {expected_ips}\n"
        f"Got: {actual_ips}"
    )

    expected_org = "Syndicate Hackers"
    actual_org = report_data["issuer_org"]
    assert actual_org == expected_org, (
        f"The 'issuer_org' string is incorrect.\n"
        f"Expected: '{expected_org}'\n"
        f"Got: '{actual_org}'"
    )