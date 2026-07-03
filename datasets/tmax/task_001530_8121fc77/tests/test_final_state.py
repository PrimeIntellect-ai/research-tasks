# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/math_project"
CRASH_LINE_TXT = os.path.join(PROJECT_DIR, "crash_line.txt")
FINAL_RESULT_TXT = os.path.join(PROJECT_DIR, "final_result.txt")
MAKEFILE = os.path.join(PROJECT_DIR, "Makefile")
CALC_EXE = os.path.join(PROJECT_DIR, "calc")
DATA_TXT = os.path.join(PROJECT_DIR, "data.txt")

def test_crash_line_saved():
    assert os.path.isfile(CRASH_LINE_TXT), f"{CRASH_LINE_TXT} is missing."
    with open(CRASH_LINE_TXT, 'r') as f:
        content = f.read().strip()
    assert "425 DIV 50 0" in content, f"crash_line.txt does not contain the correct crash line. Found: {content}"

def test_final_result_saved():
    assert os.path.isfile(FINAL_RESULT_TXT), f"{FINAL_RESULT_TXT} is missing."
    with open(FINAL_RESULT_TXT, 'r') as f:
        content = f.read().strip()
    assert "Total: 12693" in content, f"final_result.txt does not contain the correct total. Found: {content}"

def test_make_succeeds():
    assert os.path.isfile(MAKEFILE), f"{MAKEFILE} is missing."
    # Clean first if possible, though not strictly required, we can just run make
    # We will remove the executable to ensure make actually builds it
    if os.path.isfile(CALC_EXE):
        os.remove(CALC_EXE)

    result = subprocess.run(["make"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with error:\n{result.stderr}"
    assert os.path.isfile(CALC_EXE), f"make succeeded but {CALC_EXE} was not created."

def test_executable_runs_without_crash():
    assert os.path.isfile(CALC_EXE), f"{CALC_EXE} is missing, cannot test execution."
    result = subprocess.run(["./calc", "data.txt"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Program crashed or returned non-zero exit code: {result.returncode}\nStderr: {result.stderr}"
    assert "Total: 12693" in result.stdout, f"Program output did not contain 'Total: 12693'. Found: {result.stdout}"