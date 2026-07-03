# test_final_state.py

import os
import re

def test_state_tester_script():
    """Test that the state_tester.sh script exists and is executable."""
    script_path = "/home/user/state_tester.sh"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Expected script {script_path} is not executable."

def test_makefile_exists_and_target():
    """Test that the Makefile exists and contains the test-api target."""
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"Expected Makefile {makefile_path} does not exist."

    with open(makefile_path, 'r') as f:
        content = f.read()

    # Check for the test-api target definition
    assert re.search(r'^test-api:', content, re.MULTILINE), "Makefile does not contain the 'test-api' target definition."

def test_ci_output_log():
    """Test that the ci_output.log exists and contains the correct flag."""
    log_path = "/home/user/ci_output.log"
    assert os.path.isfile(log_path), f"Expected log file {log_path} does not exist. Did you run the Makefile target?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{b4sh_st4t3_m4ch1n3_m4st3r}"
    assert content == expected_flag, f"Expected {log_path} to contain exactly '{expected_flag}', but found '{content}'."