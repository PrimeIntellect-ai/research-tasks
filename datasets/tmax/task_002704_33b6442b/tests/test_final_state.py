# test_final_state.py
import os
import subprocess
import pytest

def test_proxy_cpp_compilation_and_logic():
    cpp_path = "/home/user/proxy.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."

    test_bin = "/home/user/test_proxy_pytest"
    compile_proc = subprocess.run(["g++", cpp_path, "-o", test_bin], capture_output=True)
    assert compile_proc.returncode == 0, f"Failed to compile {cpp_path}:\n{compile_proc.stderr.decode()}"

    # Test valid input
    valid_proc = subprocess.run([test_bin], input=b"COST_REQUEST_1\n", capture_output=True)
    assert valid_proc.stdout.decode().strip() == "FORWARD", "Proxy did not output 'FORWARD' for an input starting with 'COST'."

    # Test invalid input
    invalid_proc = subprocess.run([test_bin], input=b"SPAM_REQUEST_2\n", capture_output=True)
    assert invalid_proc.stdout.decode().strip() == "DROP", "Proxy did not output 'DROP' for an input not starting with 'COST'."

    # Check log file
    log_path = "/home/user/proxy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."
    with open(log_path, "r") as f:
        log_content = f.read()
    assert "[BLOCKED] SPAM_REQUEST_2" in log_content, "Log file did not contain the expected '[BLOCKED] <input>' message."

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read().lower()

    assert "daily" in content, "logrotate.conf is missing the 'daily' directive."
    assert "rotate 2" in content, "logrotate.conf is missing the 'rotate 2' directive."
    assert "compress" in content, "logrotate.conf is missing the 'compress' directive."
    assert "missingok" in content, "logrotate.conf is missing the 'missingok' directive."

def test_deploy_script():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Setup dummy active proxy if not present to allow script to run properly
    active_path = "/home/user/proxy_active"
    if not os.path.exists(active_path) and not os.path.islink(active_path):
        with open(active_path, "w") as f:
            f.write("dummy")

    # Run deployment script
    deploy_proc = subprocess.run([script_path], capture_output=True)
    assert deploy_proc.returncode == 0, f"deploy.sh failed with error:\n{deploy_proc.stderr.decode()}"

    # Verify outcomes
    backup_path = "/home/user/proxy_backup"
    v2_path = "/home/user/proxy_v2"

    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."
    assert os.path.isfile(v2_path), f"Compiled binary {v2_path} does not exist."
    assert os.path.islink(active_path), f"{active_path} is not a symbolic link."

    target = os.readlink(active_path)
    assert target == v2_path, f"Symlink {active_path} points to {target}, expected {v2_path}."