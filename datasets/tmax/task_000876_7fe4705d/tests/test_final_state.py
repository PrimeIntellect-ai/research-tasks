# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_directories_exist():
    """Verify that required directories exist."""
    dirs = [
        "/home/user/src",
        "/home/user/bin",
        "/home/user/config",
        "/home/user/logs"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_setup_env_script_and_acl_file():
    """Verify setup_env.sh works and acl.conf is correct."""
    setup_script = "/home/user/setup_env.sh"
    assert os.path.isfile(setup_script), f"{setup_script} does not exist."
    assert os.access(setup_script, os.X_OK), f"{setup_script} is not executable."

    # Run setup_env.sh to ensure it's idempotent and sets up the environment correctly
    result = subprocess.run(["bash", setup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"setup_env.sh failed with exit code {result.returncode}. stderr: {result.stderr}"

    acl_file = "/home/user/config/acl.conf"
    assert os.path.isfile(acl_file), f"{acl_file} does not exist."

    with open(acl_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    assert lines == ["10.0.0.5", "192.168.1.100"], f"acl.conf contents are incorrect: {lines}"

    st = os.stat(acl_file)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"acl.conf has incorrect permissions: {oct(perms)}, expected 0o400."

def test_ip_filter_binary():
    """Verify the C++ ip_filter binary behaves correctly."""
    binary = "/home/user/bin/ip_filter"
    log_file = "/home/user/logs/filter.log"
    assert os.path.isfile(binary), f"{binary} does not exist."
    assert os.access(binary, os.X_OK), f"{binary} is not executable."

    # Test ALLOW
    result_allow = subprocess.run([binary, "192.168.1.100"], capture_output=True)
    assert result_allow.returncode == 0, "ip_filter should return 0 for permitted IP."

    with open(log_file, "r") as f:
        logs = f.readlines()
    assert logs and "[ALLOW] 192.168.1.100" in logs[-1], "ip_filter did not append [ALLOW] correctly."

    # Test DENY
    result_deny = subprocess.run([binary, "1.1.1.1"], capture_output=True)
    assert result_deny.returncode == 1, "ip_filter should return 1 for denied IP."

    with open(log_file, "r") as f:
        logs = f.readlines()
    assert logs and "[DENY] 1.1.1.1" in logs[-1], "ip_filter did not append [DENY] correctly."

def test_rotate_script():
    """Verify rotate.sh correctly rotates logs."""
    rotate_script = "/home/user/rotate.sh"
    assert os.path.isfile(rotate_script), f"{rotate_script} does not exist."
    assert os.access(rotate_script, os.X_OK), f"{rotate_script} is not executable."

    log_dir = "/home/user/logs"
    # Create fake logs
    with open(f"{log_dir}/filter.log", "w") as f: f.write("test0\n")
    with open(f"{log_dir}/filter.log.1", "w") as f: f.write("test1\n")
    with open(f"{log_dir}/filter.log.2", "w") as f: f.write("test2\n")

    result = subprocess.run(["bash", rotate_script], capture_output=True, text=True)
    assert result.returncode == 0, f"rotate.sh failed with exit code {result.returncode}."

    # Check new filter.log
    assert os.path.isfile(f"{log_dir}/filter.log"), "New filter.log was not created."
    with open(f"{log_dir}/filter.log", "r") as f:
        assert f.read() == "", "New filter.log is not empty."

    st = os.stat(f"{log_dir}/filter.log")
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o644, f"New filter.log has incorrect permissions: {oct(perms)}, expected 0o644."

    # Check rotated logs
    with open(f"{log_dir}/filter.log.1", "r") as f:
        assert f.read().strip() == "test0", "filter.log.1 content is incorrect."
    with open(f"{log_dir}/filter.log.2", "r") as f:
        assert f.read().strip() == "test1", "filter.log.2 content is incorrect."
    with open(f"{log_dir}/filter.log.3", "r") as f:
        assert f.read().strip() == "test2", "filter.log.3 content is incorrect."

def test_diagnostics():
    """Verify test_filter.sh ran and appended correctly to diagnostics.txt."""
    diag_file = "/home/user/logs/diagnostics.txt"
    assert os.path.isfile(diag_file), f"{diag_file} does not exist."

    with open(diag_file, "r") as f:
        content = f.read()
    assert "DIAGNOSTICS_PASSED" in content, f"diagnostics.txt does not contain 'DIAGNOSTICS_PASSED'. Content: {content}"