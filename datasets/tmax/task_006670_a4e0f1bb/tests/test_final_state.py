# test_final_state.py

import os
import json
import subprocess
import pytest

def test_prepare_release_script_exists_and_executable():
    script_path = "/home/user/release/prepare_release.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_json_exists_and_valid():
    report_path = "/home/user/release/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert isinstance(data, dict), "JSON root must be an object/dictionary."
    assert "abi_secure" in data, "Missing 'abi_secure' key in report.json."
    assert "max_retries_value" in data, "Missing 'max_retries_value' key in report.json."
    assert "check_auth_offset" in data, "Missing 'check_auth_offset' key in report.json."

def test_report_json_values():
    report_path = "/home/user/release/report.json"
    with open(report_path, "r") as f:
        data = json.load(f)

    # Check abi_secure
    assert data["abi_secure"] is False, "abi_secure should be false (boolean)."

    # Check max_retries_value
    assert data["max_retries_value"] == 13, "max_retries_value should be 13 (integer)."

    # Dynamically determine check_auth_offset
    handler_path = "/home/user/release/handler.o"
    assert os.path.isfile(handler_path), f"File {handler_path} missing, cannot verify offset."

    result = subprocess.run(["objdump", "-t", handler_path], capture_output=True, text=True)
    assert result.returncode == 0, "objdump command failed."

    offset_val = None
    for line in result.stdout.splitlines():
        if "check_auth" in line:
            parts = line.split()
            if len(parts) > 0:
                # The first column is the offset
                offset_val = parts[0].lstrip("0")
                if offset_val == "":
                    offset_val = "0"
                break

    assert offset_val is not None, "Could not find 'check_auth' in objdump output."
    assert data["check_auth_offset"] == offset_val, f"check_auth_offset should be '{offset_val}'."