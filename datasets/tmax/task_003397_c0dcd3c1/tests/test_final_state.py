# test_final_state.py

import os
import re
import stat
import pytest

def test_provision_config():
    config_path = "/home/user/provision_config.txt"
    assert os.path.exists(config_path), f"Configuration file {config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "LOG_DIR=/home/user/custom_logs" in content, f"LOG_DIR not set correctly in {config_path}."
    assert "SIZE=5M" in content, f"SIZE not set correctly in {config_path}."
    assert "ROTATIONS=3" in content, f"ROTATIONS not set correctly in {config_path}."

def test_expect_script_exists():
    script_path = "/home/user/run_init.exp"
    assert os.path.exists(script_path), f"Expect script {script_path} does not exist."

def test_c_program_and_binary():
    source_path = "/home/user/create_dirs.c"
    binary_path = "/home/user/create_dirs"

    assert os.path.exists(source_path), f"C source file {source_path} does not exist."
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_filesystem_setup():
    log_dir = "/home/user/custom_logs"
    log_file = os.path.join(log_dir, "setup.log")

    assert os.path.exists(log_dir), f"Directory {log_dir} does not exist."
    assert os.path.isdir(log_dir), f"{log_dir} is not a directory."

    # Check permissions (0755)
    st = os.stat(log_dir)
    assert stat.S_IMODE(st.st_mode) == 0o755, f"Directory {log_dir} does not have 0755 permissions."

    assert os.path.exists(log_file), f"Log file {log_file} does not exist."
    assert os.path.isfile(log_file), f"{log_file} is not a regular file."

def test_logrotate_config():
    config_path = "/home/user/custom_logrotate.conf"
    assert os.path.exists(config_path), f"Logrotate config {config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    # Remove comments and normalize whitespace for easier checking
    clean_content = re.sub(r'#.*', '', content)

    # Check target pattern
    assert re.search(r'/home/user/custom_logs/\*\.log\s*\{', clean_content), \
        f"Target pattern '/home/user/custom_logs/*.log' not found or malformed in {config_path}."

    # Check directives
    assert re.search(r'\bsize\s+5[Mm]\b', clean_content) or re.search(r'\bmaxsize\s+5[Mm]\b', clean_content) or "5M" in clean_content, \
        f"Size directive (5M) not found in {config_path}."
    assert re.search(r'\brotate\s+3\b', clean_content), f"'rotate 3' not found in {config_path}."
    assert re.search(r'\bmissingok\b', clean_content), f"'missingok' not found in {config_path}."
    assert re.search(r'\bnomail\b', clean_content), f"'nomail' not found in {config_path}."