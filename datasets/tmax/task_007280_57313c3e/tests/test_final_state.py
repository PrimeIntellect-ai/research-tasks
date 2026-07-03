# test_final_state.py

import os
import json
import subprocess
import pytest

def test_debug_report_json():
    report_path = "/home/user/debug_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} is not valid JSON.")

    assert "debug_token" in data, "Key 'debug_token' is missing in the JSON report."
    assert data["debug_token"] == "a1b2c3d4-8f9e-4a5b-9c8d-7e6f5a4b3c2d", "Incorrect debug_token in JSON report."

    assert "crash_fragment" in data, "Key 'crash_fragment' is missing in the JSON report."
    assert data["crash_fragment"] == "critical", "Incorrect crash_fragment in JSON report."

def test_scan_script_fixed():
    script_path = "/home/user/service_repo/scan.sh"
    repo_dir = "/home/user/service_repo"

    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    try:
        result = subprocess.run(
            [script_path],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script {script_path} failed to execute properly. Return code: {e.returncode}\nOutput: {e.stdout}\nError: {e.stderr}")

    output = result.stdout + result.stderr

    # The original buggy script outputs "Error: data/critical not found."
    # The fixed script should not output any errors related to file not found.
    assert "Error:" not in output, f"Script output contains errors, indicating it still fails on spaces:\n{output}"
    assert "not found" not in output, f"Script output contains 'not found', indicating it still fails on spaces:\n{output}"

    # Ensure it actually ran and did something (did not just exit empty)
    assert "Processing" in output or "backup.tar.gz" in output or "report 2023.dat" in output, "Script did not seem to process the files as expected."