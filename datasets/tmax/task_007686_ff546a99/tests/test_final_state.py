# test_final_state.py

import os
import subprocess
import pytest

def test_forensics_report():
    report_path = "/home/user/forensics_report.txt"
    assert os.path.exists(report_path), f"Report file missing at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Report file {report_path} must contain at least 2 lines."

    assert lines[0] == "TX-99842", f"Line 1 of report should be exactly 'TX-99842', got '{lines[0]}'."
    assert lines[1] in ["0", "0.0"], f"Line 2 of report should be '0' or '0.0', got '{lines[1]}'."

def test_cargo_test_passes():
    project_dir = "/home/user/trade_analyzer"
    assert os.path.exists(project_dir), f"Project directory missing at {project_dir}"

    try:
        result = subprocess.run(
            ["cargo", "test"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        assert result.returncode == 0, f"`cargo test` failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except FileNotFoundError:
        pytest.fail("cargo command not found. Is Rust installed?")

def test_cargo_run_output():
    project_dir = "/home/user/trade_analyzer"

    try:
        result = subprocess.run(
            ["cargo", "run", "--", "--tx", "TX-99842"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        assert result.returncode == 0, f"`cargo run` failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        output = result.stdout.strip()
        assert output in ["0", "0.0"], f"Expected output '0' or '0.0' for TX-99842, got '{output}'"
    except FileNotFoundError:
        pytest.fail("cargo command not found.")