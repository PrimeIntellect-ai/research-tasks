# test_final_state.py

import os
import stat
import pytest

def test_capacity_report_exists_and_correct():
    report_path = "/home/user/capacity_report.eml"
    assert os.path.exists(report_path), f"Expected report file {report_path} does not exist."

    expected_content = (
        "To: admin@example.com\n"
        "From: planner@example.com\n"
        "Subject: Capacity Report\n"
        "Date: Wed, 23 Oct 2024 15:00:00 +0900\n"
        "\n"
        "Environment: dev\n"
        "Total Memory: 256 MB\n"
        "Total CPU: 10.0%\n"
        "\n"
        "Environment: prod\n"
        "Total Memory: 1600 MB\n"
        "Total CPU: 115.5%\n"
    )

    with open(report_path, "r") as f:
        actual_content = f.read()

    # Standardize line endings for comparison
    actual_content = actual_content.replace('\r\n', '\n').strip()
    expected_content = expected_content.strip()

    assert actual_content == expected_content, f"Content of {report_path} does not match the expected format or values.\nExpected:\n{expected_content}\n\nActual:\n{actual_content}"

def test_kill_script_exists_and_correct():
    script_path = "/home/user/kill_high_cpu.sh"
    assert os.path.exists(script_path), f"Expected script file {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    expected_lines = [
        "#!/bin/bash",
        "kill -9 1001"
    ]

    with open(script_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines[0] == expected_lines[0], f"First line of {script_path} must be {expected_lines[0]}"

    # The order of kill commands might technically vary if there were multiple, but here there's only 1001.
    assert "kill -9 1001" in actual_lines, f"Expected 'kill -9 1001' in {script_path}"

    # Ensure no other pids are killed
    kills = [line for line in actual_lines if line.startswith("kill ")]
    assert len(kills) == 1, f"Expected exactly 1 kill command in {script_path}, found {len(kills)}"