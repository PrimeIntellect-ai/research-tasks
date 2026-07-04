# test_final_state.py

import os
import stat

def test_runner_script_exists_and_executable():
    """Check that /home/user/runner.sh exists and is executable."""
    script_path = "/home/user/runner.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_execution_log_content():
    """Check that /home/user/execution.log contains the expected output."""
    log_path = "/home/user/execution.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did the script run successfully?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Strict Policy Enforced: Target Delta"
    assert content == expected_content, f"Expected '{expected_content}' in {log_path}, got '{content}'"

def test_runner_script_contains_security_constraints():
    """Verify that runner.sh uses env -i and timeout 5 to isolate and constrain the process."""
    script_path = "/home/user/runner.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "env -i" in content, "The script does not appear to use 'env -i' for environment isolation."
    assert "timeout 5" in content, "The script does not appear to use 'timeout 5' for execution constraint."