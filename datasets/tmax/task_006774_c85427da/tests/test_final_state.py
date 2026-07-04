# test_final_state.py

import os
import re
import pytest

def test_server_c_fixed():
    """Test that the server.c file has been fixed to not truncate the path to 10 chars."""
    server_c_path = '/home/user/app/server.c'
    assert os.path.isfile(server_c_path), f"File {server_c_path} does not exist."

    with open(server_c_path, 'r') as f:
        content = f.read()

    # The bug was strncpy(addr.sun_path, env_path, 10);
    assert "strncpy(addr.sun_path, env_path, 10);" not in content, "The bug (strncpy(..., 10)) is still present in server.c."

    # Check that it copies the env_path to addr.sun_path
    assert "addr.sun_path" in content and "env_path" in content, "Missing assignment to addr.sun_path from env_path."

def test_server_compiled():
    """Test that the server executable has been compiled."""
    server_path = '/home/user/app/server'
    assert os.path.isfile(server_path), f"Executable {server_path} does not exist."
    assert os.access(server_path, os.X_OK), f"File {server_path} is not executable."

def test_bashrc_exports():
    """Test that .bashrc contains the correct exports."""
    bashrc_path = '/home/user/.bashrc'
    assert os.path.isfile(bashrc_path), f"File {bashrc_path} does not exist."

    with open(bashrc_path, 'r') as f:
        content = f.read()

    # Use regex to allow for potential whitespace variations or quotes
    assert re.search(r'export\s+UPSTREAM_SOCKET=[\'"]?/home/user/run/microservice\.sock[\'"]?', content), \
        "UPSTREAM_SOCKET export is missing or incorrect in .bashrc."
    assert re.search(r'export\s+TZ=[\'"]?Etc/UTC[\'"]?', content), \
        "TZ export is missing or incorrect in .bashrc."

def test_ci_test_sh_exists_and_executable():
    """Test that ci_test.sh exists, is executable, and has expected commands."""
    script_path = '/home/user/ci_test.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, 'r') as f:
        content = f.read()

    assert ".bashrc" in content, "ci_test.sh does not source .bashrc."
    assert "server" in content, "ci_test.sh does not start the server."
    assert "nc -U" in content, "ci_test.sh does not use 'nc -U' to connect to the socket."
    assert "ci_result.log" in content, "ci_test.sh does not redirect output to ci_result.log."

def test_ci_result_log():
    """Test that the CI result log exists and contains the expected output."""
    log_path = '/home/user/ci_result.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run ci_test.sh?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert content == "OK\n", f"Expected log content to be 'OK\\n', but got {repr(content)}"