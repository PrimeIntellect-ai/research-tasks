# test_final_state.py

import os
import subprocess
import pytest

def test_report_txt():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 3, f"Expected exactly 3 lines in {report_path}, found {len(lines)}."
    assert lines[0] == "REQ-1004", f"Line 1 of report.txt is incorrect. Expected 'REQ-1004', got '{lines[0]}'."
    assert lines[1] == "FF41", f"Line 2 of report.txt is incorrect. Expected 'FF41', got '{lines[1]}'."
    assert lines[2] == "FIXED", f"Line 3 of report.txt is incorrect. Expected 'FIXED', got '{lines[2]}'."

def test_bad_payload_bin():
    payload_path = "/home/user/bad_payload.bin"
    assert os.path.isfile(payload_path), f"File {payload_path} does not exist."

    with open(payload_path, "rb") as f:
        content = f.read()

    assert len(content) == 2, f"Expected {payload_path} to be exactly 2 bytes, but it is {len(content)} bytes."
    assert content[0] == 0xFF, f"First byte of {payload_path} is incorrect. Expected 0xFF."
    assert content[1] == 0x41, f"Second byte of {payload_path} is incorrect. Expected 0x41."

def test_telemetry_parser_executable():
    bin_path = "/home/user/bin/telemetry_parser"
    assert os.path.isfile(bin_path), f"Executable {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_telemetry_parser_execution():
    bin_path = "/home/user/bin/telemetry_parser"
    payload_path = "/home/user/bad_payload.bin"

    assert os.path.isfile(bin_path), "Executable missing, cannot test execution."
    assert os.path.isfile(payload_path), "Payload file missing, cannot test execution."

    try:
        result = subprocess.run(
            [bin_path, payload_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The executable timed out after 1 second. The livelock bug is likely not fixed.")

    assert result.returncode == 0, f"Executable returned non-zero exit code: {result.returncode}. Stderr: {result.stderr.decode()}"