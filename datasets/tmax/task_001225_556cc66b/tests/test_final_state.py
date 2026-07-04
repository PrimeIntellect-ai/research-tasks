# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/packet_project"
REPORT_FILE = "/home/user/report.txt"
FUZZ_SCRIPT = os.path.join(PROJECT_DIR, "fuzz.sh")
PARSER_C = os.path.join(PROJECT_DIR, "parser.c")

def test_make_test_success():
    """Check if make test runs successfully with exit code 0."""
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} is missing."
    result = subprocess.run(["make", "test"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"'make test' failed. stdout: {result.stdout}, stderr: {result.stderr}"

def test_report_content():
    """Check if report.txt contains the correct packet number and function name."""
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} is missing."
    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 2, f"Expected exactly 2 lines in {REPORT_FILE}, found {len(lines)}."
    assert lines[0] == "7", f"Expected packet number '7' on line 1, found '{lines[0]}'."
    assert lines[1] == "process_payload", f"Expected function 'process_payload' on line 2, found '{lines[1]}'."

def test_fuzz_script_exists_and_executable():
    """Check if fuzz.sh exists and is executable."""
    assert os.path.isfile(FUZZ_SCRIPT), f"Fuzzer script {FUZZ_SCRIPT} is missing."
    assert os.access(FUZZ_SCRIPT, os.X_OK), f"Fuzzer script {FUZZ_SCRIPT} is not executable."

def test_parser_c_modified_but_retains_core_logic():
    """Check if parser.c still contains core logic."""
    assert os.path.isfile(PARSER_C), f"Source file {PARSER_C} is missing."
    with open(PARSER_C, "r") as f:
        content = f.read()
    assert "process_payload" in content, "Core logic function 'process_payload' was removed from parser.c."