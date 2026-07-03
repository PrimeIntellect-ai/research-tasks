# test_final_state.py

import os
import json
import subprocess
import hashlib
import pytest

def test_generate_report_script_exists():
    script_path = "/home/user/generate_report.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_incident_report_json():
    report_path = "/home/user/incident_report.json"
    assert os.path.isfile(report_path), f"The incident report {report_path} was not generated."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected_token = "sec_t0k3n_99f2a1"
    expected_path = "/home/user/drop/payload.elf"

    # Compute expected hash
    with open(expected_path, "rb") as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    # Compute expected architecture
    try:
        out_arch = subprocess.check_output(["readelf", "-h", expected_path]).decode("utf-8")
        expected_arch = [line.split("Machine:")[1].strip() for line in out_arch.split("\n") if "Machine:" in line][0]
    except Exception as e:
        pytest.fail(f"Could not read ELF architecture from {expected_path}: {e}")

    assert data.get("leaked_token") == expected_token, f"Expected leaked_token to be '{expected_token}', got '{data.get('leaked_token')}'."
    assert data.get("payload_path") == expected_path, f"Expected payload_path to be '{expected_path}', got '{data.get('payload_path')}'."
    assert data.get("payload_sha256") == expected_hash, f"Expected payload_sha256 to be '{expected_hash}', got '{data.get('payload_sha256')}'."

    actual_arch = data.get("elf_architecture", "")
    assert expected_arch.lower() in actual_arch.lower() or actual_arch.lower() in expected_arch.lower(), \
        f"Expected elf_architecture to match '{expected_arch}', got '{actual_arch}'."