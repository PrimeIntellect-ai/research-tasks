# test_final_state.py

import os
import pytest

def test_deployment_success_log_exists():
    """Check if the deployment_success.log file was generated."""
    log_path = "/home/user/deployment_success.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing. The expect script may not have been executed successfully."

def test_deployment_success_log_content():
    """Check if the deployment_success.log contains the correct success message."""
    log_path = "/home/user/deployment_success.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_content = "SUCCESS: Blocked 192.168.1.105 in staged environment"
    assert content == expected_content, f"Content of {log_path} is incorrect. Expected '{expected_content}', got '{content}'."

def test_expect_script_exists_and_shebang():
    """Check if the expect script exists and has the correct shebang."""
    script_path = "/home/user/auto_deploy.exp"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    with open(script_path, 'r') as f:
        first_line = f.readline().strip()

    assert first_line == "#!/usr/bin/expect", f"The expect script {script_path} does not have the correct shebang. Expected '#!/usr/bin/expect', got '{first_line}'."

def test_expect_script_content():
    """Check if the expect script calls the correct script."""
    script_path = "/home/user/auto_deploy.exp"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "/home/user/deploy_fw" in content or "deploy_fw" in content, f"The expect script does not appear to spawn the target deployment script."