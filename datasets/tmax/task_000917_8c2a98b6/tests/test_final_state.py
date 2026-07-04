# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/process_translations.sh"
CLEAN_CSV = "/home/user/clean_translations.csv"
METRICS_FILE = "/home/user/gate_metrics.txt"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_exit_code():
    # Remove output files if they exist to ensure we test the script's execution
    if os.path.exists(CLEAN_CSV):
        os.remove(CLEAN_CSV)
    if os.path.exists(METRICS_FILE):
        os.remove(METRICS_FILE)

    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script exited with code {result.returncode}, expected 0. stderr: {result.stderr}"

def test_gate_metrics():
    assert os.path.exists(METRICS_FILE), f"{METRICS_FILE} was not created."
    with open(METRICS_FILE, "r") as f:
        content = f.read().strip()
    assert content == "3", f"Expected gate_metrics.txt to contain '3', but got '{content}'."

def test_clean_translations():
    assert os.path.exists(CLEAN_CSV), f"{CLEAN_CSV} was not created."
    with open(CLEAN_CSV, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines in {CLEAN_CSV}, got {len(lines)}."

    expected_lines = [
        "HOME_BTN,en-US,Home,1600000000,APPROVED",
        "SUBMIT_BTN,fr-FR,Soumettre,1600000010,APPROVED",
        "SETTINGS,en-US,Settings,1600000050,APPROVED",
        "HELP_BTN,en-US,Help me,1600000065,APPROVED",
        "DASHBOARD,es-ES,Tablero de mandos,1600000080,DRAFT"
    ]

    assert sorted(lines) == sorted(expected_lines), "The contents of clean_translations.csv do not match the expected output."