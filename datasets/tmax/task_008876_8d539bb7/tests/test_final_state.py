# test_final_state.py

import os
import json
import subprocess
import time
import pytest

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "cwe_id" in data, "Missing 'cwe_id' in report.json"
    assert data["cwe_id"] == "CWE-22", f"Expected cwe_id to be 'CWE-22', got '{data['cwe_id']}'"

    assert "xor_key" in data, "Missing 'xor_key' in report.json"
    assert data["xor_key"] == "irks", f"Expected xor_key to be 'irks', got '{data['xor_key']}'"

    assert "flag" in data, "Missing 'flag' in report.json"
    assert data["flag"] == "FLAG{tr4v3rs4l_m4lw4r3_f0und}", f"Expected flag to be 'FLAG{{tr4v3rs4l_m4lw4r3_f0und}}', got '{data['flag']}'"

def test_poc_execution():
    poc_path = "/home/user/poc.py"
    assert os.path.isfile(poc_path), f"PoC script {poc_path} does not exist."

    server_path = "/home/user/app/server.py"
    assert os.path.isfile(server_path), f"Server script {server_path} is missing."

    success_file = "/home/user/success.txt"
    if os.path.exists(success_file):
        os.remove(success_file)

    # Start the server
    server_proc = subprocess.Popen(
        ["python3", server_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        # Give the server a moment to start
        time.sleep(2)

        # Run the PoC script
        result = subprocess.run(
            ["python3", poc_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, f"PoC script failed to execute. stderr: {result.stderr}"

        # Verify the success file was created and contains the correct content
        assert os.path.isfile(success_file), f"PoC did not create {success_file}."

        with open(success_file, "r") as f:
            content = f.read().strip()

        assert content == "EXPLOITED", f"Expected {success_file} to contain 'EXPLOITED', got '{content}'"

    finally:
        server_proc.terminate()
        server_proc.wait()