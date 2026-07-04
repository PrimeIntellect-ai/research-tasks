# test_final_state.py

import os
import pytest

def test_cpp_source_exists():
    """Verify that the C++ source file exists."""
    cpp_path = "/home/user/src/tcp_ping.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."

def test_bash_script_exists_and_executable():
    """Verify that the bash script exists and is executable."""
    script_path = "/home/user/run_checks.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

def test_binary_exists_and_executable():
    """Verify that the compiled C++ binary exists and is executable."""
    bin_path = "/home/user/bin/tcp_ping"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"Compiled binary {bin_path} is not executable."

def test_uptime_log_contents():
    """Verify that the uptime.log file contains exactly the expected UP and DOWN sequence."""
    log_path = "/home/user/uptime.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "UP\nDOWN"
    assert content == expected_content, f"Log file contents do not match expected sequence. Expected:\n{expected_content}\nActual:\n{content}"