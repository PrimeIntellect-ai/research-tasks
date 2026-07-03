# test_final_state.py

import os
import random
import string
import subprocess
import socket
import threading
import time
import pytest
import shutil

ORACLE_PATH = "/app/legacy_processor"
AGENT_SCRIPT = "/home/user/new_processor.py"
CHECK_SCRIPT = "/home/user/check_and_run.sh"
LOGROTATE_CONF = "/home/user/logrotate.conf"
REPO_DIR = "/home/user/migration_repo"
PRE_COMMIT_HOOK = os.path.join(REPO_DIR, ".git/hooks/pre-commit")

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Missing agent script at {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_PATH), f"Missing oracle binary at {ORACLE_PATH}"

    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !@#$%^&*()_+-=[]{}|;':,./<>?"
    random.seed(42)

    for _ in range(1000):
        length = random.randint(1, 1000)
        input_str = "".join(random.choices(charset, k=length))
        input_bytes = input_str.encode('utf-8')

        # Run oracle
        oracle_proc = subprocess.run([ORACLE_PATH], input=input_bytes, capture_output=True)
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(["python3", AGENT_SCRIPT], input=input_bytes, capture_output=True)
        agent_out = agent_proc.stdout

        assert oracle_out == agent_out, (
            f"Output mismatch for input: {input_str!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output: {agent_out!r}"
        )

def test_check_and_run_script_port_closed():
    assert os.path.isfile(CHECK_SCRIPT), f"Missing script at {CHECK_SCRIPT}"
    assert os.access(CHECK_SCRIPT, os.X_OK), f"Script is not executable: {CHECK_SCRIPT}"

    error_log = "/home/user/processed/error.log"
    if os.path.exists(error_log):
        os.remove(error_log)

    subprocess.run([CHECK_SCRIPT], shell=True, executable="/bin/bash")

    assert os.path.exists(error_log), f"Missing error log: {error_log}"
    with open(error_log, "r") as f:
        content = f.read()
    assert "ERROR: Port 8080 unreachable" in content, "Error log does not contain correct message"

def test_check_and_run_script_port_open():
    master_log = "/home/user/processed/master.log"
    if os.path.exists(master_log):
        os.remove(master_log)

    # Start a dummy server on port 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080))
    server.listen(1)

    def accept_conn():
        try:
            server.settimeout(5)
            conn, _ = server.accept()
            conn.close()
        except socket.timeout:
            pass

    t = threading.Thread(target=accept_conn)
    t.start()

    try:
        subprocess.run([CHECK_SCRIPT], shell=True, executable="/bin/bash")
    finally:
        server.close()
        t.join()

    assert os.path.exists(master_log), f"Missing master log: {master_log}"

def test_logrotate_conf():
    assert os.path.isfile(LOGROTATE_CONF), f"Missing logrotate.conf at {LOGROTATE_CONF}"
    with open(LOGROTATE_CONF, "r") as f:
        content = f.read().lower()

    assert "daily" in content, "Missing 'daily' directive in logrotate.conf"
    assert "rotate 7" in content, "Missing 'rotate 7' directive in logrotate.conf"
    assert "compress" in content, "Missing 'compress' directive in logrotate.conf"
    assert "delaycompress" in content, "Missing 'delaycompress' directive in logrotate.conf"
    assert "missingok" in content, "Missing 'missingok' directive in logrotate.conf"

def test_git_pre_commit_hook():
    assert os.path.isdir(REPO_DIR), f"Missing git repo at {REPO_DIR}"
    assert os.path.isdir(os.path.join(REPO_DIR, ".git")), f"Not a git repository: {REPO_DIR}"
    assert os.path.isfile(PRE_COMMIT_HOOK), f"Missing pre-commit hook at {PRE_COMMIT_HOOK}"
    assert os.access(PRE_COMMIT_HOOK, os.X_OK), f"pre-commit hook is not executable"

    # Test valid commit
    test_file_valid = os.path.join(REPO_DIR, "test_valid.py")
    with open(test_file_valid, "w") as f:
        f.write("print('Hello World')\n")

    subprocess.run(["git", "add", "test_valid.py"], cwd=REPO_DIR, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=REPO_DIR)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=REPO_DIR)

    res_valid = subprocess.run(["git", "commit", "-m", "Valid commit"], cwd=REPO_DIR, capture_output=True, text=True)
    assert res_valid.returncode == 0, f"Valid commit was rejected: {res_valid.stderr}"

    # Test invalid commit
    test_file_invalid = os.path.join(REPO_DIR, "test_invalid.py")
    with open(test_file_invalid, "w") as f:
        f.write("DEBUG_MODE=True\n")

    subprocess.run(["git", "add", "test_invalid.py"], cwd=REPO_DIR, check=True)
    res_invalid = subprocess.run(["git", "commit", "-m", "Invalid commit"], cwd=REPO_DIR, capture_output=True, text=True)

    assert res_invalid.returncode == 1, "Commit with DEBUG_MODE=True was not rejected"
    assert "No debug code allowed!" in res_invalid.stdout or "No debug code allowed!" in res_invalid.stderr, "Hook did not print the correct error message"