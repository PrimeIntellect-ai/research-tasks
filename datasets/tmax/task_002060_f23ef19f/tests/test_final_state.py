# test_final_state.py

import os
import subprocess
import pytest

def test_evaluation_results_log():
    """Test that evaluation_results.log contains the correctly formatted results."""
    log_path = "/home/user/evaluation_results.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you run the client script?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "15 + 20 = 35",
        "100 / 3 = 33.33333333333333333333",
        "50 * 2 = 100",
        "7 / 2 = 3.50000000000000000000"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {log_path}"

def test_start_server_sh_updated():
    """Test that start_server.sh was updated to handle the --py3 flag."""
    script_path = "/home/user/start_server.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "--py3" in content or "$1" in content or "$@" in content, f"Script {script_path} does not seem to check for arguments."
    assert "python3" in content, f"Script {script_path} does not contain 'python3' for the --py3 flag."
    assert "python2" in content, f"Script {script_path} does not contain 'python2' as the default fallback."

def test_ws_client_sh_exists():
    """Test that ws_client.sh was created and uses expected tools."""
    script_path = "/home/user/ws_client.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "websocat" in content, f"Script {script_path} does not use 'websocat'."
    assert "bc" in content, f"Script {script_path} does not use 'bc' for fallback evaluation."
    assert "MIGRATION_ERROR" in content, f"Script {script_path} does not check for 'MIGRATION_ERROR'."