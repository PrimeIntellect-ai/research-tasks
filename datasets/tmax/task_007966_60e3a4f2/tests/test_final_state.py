# test_final_state.py

import os
import json
import pytest

def test_failing_ips_file():
    path = "/home/user/failing_ips.txt"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_ips = ["10.0.5.12", "10.0.5.19", "10.0.5.24"]
    assert lines == expected_ips, f"Contents of {path} do not match the expected IPs. Got: {lines}"

def test_failing_errors_file():
    path = "/home/user/failing_errors.txt"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_errors = ["ERR-503", "ERR-RESET", "ERR-TIMEOUT"]
    assert lines == expected_errors, f"Contents of {path} do not match the expected error codes. Got: {lines}"

def test_container_fstab_file():
    path = "/home/user/container_fstab"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"{path} should contain exactly one line, but found {len(lines)} lines."

    fields = lines[0].split()
    assert len(fields) >= 6, f"The line in {path} does not have enough fields."

    assert fields[0] == "/home/user/shared_data", f"Expected source directory '/home/user/shared_data', got {fields[0]}"
    assert fields[1] == "/mnt/service_data", f"Expected target directory '/mnt/service_data', got {fields[1]}"
    assert fields[2] == "bind", f"Expected filesystem type 'bind', got {fields[2]}"
    assert fields[3] == "ro,nosuid", f"Expected mount options 'ro,nosuid', got {fields[3]}"
    assert fields[4] == "0", f"Expected dump value '0', got {fields[4]}"
    assert fields[5] == "0", f"Expected pass value '0', got {fields[5]}"

def test_diag_report_json():
    path = "/home/user/diag_report.json"
    assert os.path.exists(path), f"File {path} is missing."

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {path} does not contain valid JSON.")

    expected_data = {
        "10.0.5.12": "unreachable",
        "10.0.5.19": "unreachable",
        "10.0.5.24": "unreachable"
    }

    assert data == expected_data, f"Contents of {path} do not match the expected JSON structure. Got: {data}"

def test_scripts_exist():
    get_endpoints_path = "/home/user/get_endpoints.py"
    diagnose_path = "/home/user/diagnose.py"

    assert os.path.exists(get_endpoints_path), f"Script {get_endpoints_path} is missing."
    assert os.path.exists(diagnose_path), f"Script {diagnose_path} is missing."