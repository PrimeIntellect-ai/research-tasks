# test_final_state.py
import os
import subprocess
import pytest

def test_report_exists_and_correct():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} was not created."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, found {len(lines)}."

    expected_path = "/tmp/telemetry_BBCD.sock"
    expected_payload = "BBCDEVGH"

    assert lines[0] == expected_path, f"Line 1: Expected '{expected_path}', got '{lines[0]}'."
    assert lines[1] == expected_payload, f"Line 2: Expected '{expected_payload}', got '{lines[1]}'."

def test_go_code_compiles_and_runs():
    go_file = "/home/user/suspicious_parser.go"
    assert os.path.isfile(go_file), f"Source file {go_file} is missing."

    # Check if it compiles
    compile_result = subprocess.run(["go", "build", "-o", "/tmp/suspicious_parser", go_file], capture_output=True, text=True)
    assert compile_result.returncode == 0, f"Go compilation failed:\n{compile_result.stderr}"

    # Check if it runs without crashing (infinite recursion fixed)
    run_result = subprocess.run(["/tmp/suspicious_parser"], capture_output=True, text=True, timeout=5)
    assert run_result.returncode == 0, f"Program execution failed or crashed:\n{run_result.stderr}"