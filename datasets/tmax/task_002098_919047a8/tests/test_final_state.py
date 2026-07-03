# test_final_state.py

import os
import pytest

def test_results_log_exists():
    """Test that the results.log file was created."""
    log_file = "/home/user/results.log"
    assert os.path.isfile(log_file), f"File {log_file} was not created. The program may not have been run or crashed."

def test_results_log_content():
    """Test that the results.log file contains the correct deterministic output."""
    log_file = "/home/user/results.log"
    with open(log_file, 'r') as f:
        content = f.read().strip()

    expected_output = "Total StdDev Sum: 0.000000"
    assert expected_output in content, f"Expected '{expected_output}' in {log_file}, but got: '{content}'"

def test_source_code_fixes():
    """Test that the source code contains evidence of synchronization fixes."""
    sim_file = "/home/user/src/simulation.c"
    assert os.path.isfile(sim_file), f"Source file {sim_file} is missing."

    with open(sim_file, 'r') as f:
        content = f.read()

    # Check for mutex lock usage which indicates the race condition was addressed
    assert "pthread_mutex_lock" in content, "The source code does not contain 'pthread_mutex_lock'. The race condition must be fixed using the provided mutex."
    assert "pthread_mutex_unlock" in content, "The source code does not contain 'pthread_mutex_unlock'."