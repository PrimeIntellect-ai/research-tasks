# test_final_state.py

import os
import pytest

def test_report_exists_and_content():
    report_path = '/home/user/report.txt'
    assert os.path.isfile(report_path), f"{report_path} is missing. The script did not generate the report."

    with open(report_path, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "COMMIT_SHA: f9a8b7c6",
        "RUST_ERROR_CODE: E0382",
        "RUST_ERROR_LINE: 42",
        "test_duration: 115",
        "coverage: 85"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    for expected in expected_lines:
        assert expected in actual_lines, f"Expected line '{expected}' not found in {report_path}."

def test_makefile_fixed_exists_and_content():
    makefile_path = '/home/user/ci_data/Makefile.fixed'
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing. The Makefile was not fixed."

    with open(makefile_path, 'r') as f:
        content = f.read()

    lines = content.splitlines()
    assert len(lines) >= 2, f"{makefile_path} does not have enough lines."

    assert lines[0].strip() == "all: main.c", "First line of Makefile.fixed is incorrect."

    # Check for tab and -Wall
    assert lines[1].startswith("\tgcc"), "Second line of Makefile.fixed must start with a tab character followed by 'gcc'."
    assert "-Wall" in lines[1], "Second line of Makefile.fixed must contain '-Wall' instead of '-wall'."
    assert "-wall" not in lines[1], "Second line of Makefile.fixed still contains the invalid '-wall' flag."

def test_pipeline_tool_executable():
    script_path = '/home/user/pipeline_tool.sh'
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."