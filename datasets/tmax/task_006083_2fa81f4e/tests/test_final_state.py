# test_final_state.py

import os
import pytest

def test_check_convergence_script_exists_and_executable():
    script_path = '/home/user/check_convergence.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_diverged_sims_log_contents():
    log_path = '/home/user/diverged_sims.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the script?"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ['protein_B.fasta', 'protein_D.fasta']

    assert lines == expected_lines, (
        f"Contents of {log_path} are incorrect.\n"
        f"Expected: {expected_lines}\n"
        f"Found: {lines}"
    )