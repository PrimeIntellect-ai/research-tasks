# test_final_state.py
import os
import subprocess
import time

def test_bare_repo_exists():
    """Check that the bare git repository exists."""
    assert os.path.isdir("/home/user/iot_update.git/refs"), "Bare git repository /home/user/iot_update.git does not exist or is not a bare repo"

def test_post_receive_hook_executable():
    """Check that the post-receive hook exists and is executable."""
    hook_path = "/home/user/iot_update.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook {hook_path} does not exist"
    assert os.access(hook_path, os.X_OK), f"Hook {hook_path} is not executable"

def test_deployed_files_exist():
    """Check that the deployed files exist and have correct permissions."""
    assert os.path.isfile("/home/user/deploy/parser.c"), "/home/user/deploy/parser.c does not exist"

    parser_path = "/home/user/deploy/parser"
    assert os.path.isfile(parser_path), f"{parser_path} does not exist"
    assert os.access(parser_path, os.X_OK), f"{parser_path} is not executable"

    supervisor_path = "/home/user/deploy/supervisor.sh"
    assert os.path.isfile(supervisor_path), f"{supervisor_path} does not exist"
    assert os.access(supervisor_path, os.X_OK), f"{supervisor_path} is not executable"

def test_processed_log_contents():
    """Check the contents of the processed.log file for correct formatting and logic."""
    log_path = "/home/user/processed.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist"

    with open(log_path, "r") as f:
        content = f.read()

    assert "VALIDATED: [2023-11-15 06:13:20] 24.5" in content, "Missing expected translated timestamp and value for 1700000000"
    assert "VALIDATED: [2023-11-15 06:13:30] 23.9" in content, "Missing expected translated timestamp and value for 1700000010"
    assert "VALIDATED: [2023-11-15 06:13:40] 24.1" in content, "Missing expected translated timestamp and value for 1700000020"
    assert "RESTARTING PARSER" in content, "Missing 'RESTARTING PARSER' message in log"
    assert "ANOMALY" not in content, "Log contains 'ANOMALY', which should have been filtered out"

def test_supervisor_running():
    """Check that the supervisor.sh process is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "supervisor.sh"]).decode("utf-8")
        assert len(output.strip()) > 0, "supervisor.sh process is not running"
    except subprocess.CalledProcessError:
        assert False, "supervisor.sh process is not running"