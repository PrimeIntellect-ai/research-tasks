# test_final_state.py

import os
import re
import pytest

WORKSPACE_DIR = '/home/user/workspace'
PYTHON_SCRIPT = os.path.join(WORKSPACE_DIR, 'fft_mpi.py')
BASH_SCRIPT = os.path.join(WORKSPACE_DIR, 'run_profiling.sh')
RESULTS_FILE = os.path.join(WORKSPACE_DIR, 'scaling_results.txt')

def test_scripts_exist():
    """Test that the required scripts have been created."""
    assert os.path.isfile(PYTHON_SCRIPT), f"Python script {PYTHON_SCRIPT} is missing."
    assert os.path.isfile(BASH_SCRIPT), f"Bash script {BASH_SCRIPT} is missing."

def test_bash_script_executable():
    """Test that the bash script is executable."""
    assert os.access(BASH_SCRIPT, os.X_OK), f"Bash script {BASH_SCRIPT} is not executable."

def test_results_file_exists():
    """Test that the results file was generated."""
    assert os.path.isfile(RESULTS_FILE), f"Results file {RESULTS_FILE} is missing. Did you run the bash script?"

def test_results_file_content():
    """Test that the results file contains the correct output format and values."""
    with open(RESULTS_FILE, 'r') as f:
        content = f.read()

    expected_patterns = [
        r"Cores:\s*1,\s*Average Peak Index:\s*1024\.00",
        r"Cores:\s*2,\s*Average Peak Index:\s*512\.00",
        r"Cores:\s*4,\s*Average Peak Index:\s*256\.00"
    ]

    for pattern in expected_patterns:
        match = re.search(pattern, content)
        assert match is not None, (
            f"Could not find expected output matching '{pattern}' in {RESULTS_FILE}.\n"
            f"File content:\n{content}"
        )