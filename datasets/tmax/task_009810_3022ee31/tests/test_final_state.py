# test_final_state.py
import os
import re
import pytest

PRIV_ESC_FILE = "/home/user/priv_escalation.txt"
EXTRACTED_CONFIG_FILE = "/home/user/extracted_config.txt"
SAFE_RUN_SCRIPT = "/home/user/safe_run.sh"

def test_priv_escalation_identification():
    assert os.path.isfile(PRIV_ESC_FILE), f"The file {PRIV_ESC_FILE} does not exist."
    with open(PRIV_ESC_FILE, "r") as f:
        content = f.read().strip()

    expected_line = "ExecStartPre=+/bin/chmod +s /home/user/investigation/data_worker"
    assert content == expected_line, f"The content of {PRIV_ESC_FILE} is incorrect. Expected the exact ExecStartPre line."

def test_extracted_config():
    assert os.path.isfile(EXTRACTED_CONFIG_FILE), f"The file {EXTRACTED_CONFIG_FILE} does not exist."
    with open(EXTRACTED_CONFIG_FILE, "r") as f:
        content = f.read().strip()

    expected_ip = "198.51.100.45:1337"
    assert content == expected_ip, f"The content of {EXTRACTED_CONFIG_FILE} is incorrect. Expected the extracted IP and port."

def test_safe_run_script_exists_and_executable():
    assert os.path.isfile(SAFE_RUN_SCRIPT), f"The script {SAFE_RUN_SCRIPT} does not exist."
    assert os.access(SAFE_RUN_SCRIPT, os.X_OK), f"The script {SAFE_RUN_SCRIPT} is not executable."

def test_safe_run_script_content():
    with open(SAFE_RUN_SCRIPT, "r") as f:
        content = f.read()

    assert "bwrap" in content, "The script does not use bwrap (Bubblewrap)."

    # Check for read-only bind mounts
    assert re.search(r"--ro-bind\s+/usr\s+/usr", content), "Missing --ro-bind for /usr."
    assert re.search(r"--ro-bind\s+/lib\s+/lib", content), "Missing --ro-bind for /lib."
    assert re.search(r"--ro-bind\s+/home/user/investigation\s+/home/user/investigation", content), "Missing --ro-bind for /home/user/investigation."

    # Check for tmpfs
    assert re.search(r"--tmpfs\s+/tmp", content), "Missing --tmpfs for /tmp."

    # Check for namespace unsharing
    has_unshare_all = "--unshare-all" in content
    has_individual_unshares = all(flag in content for flag in [
        "--unshare-user", "--unshare-ipc", "--unshare-pid", "--unshare-net", "--unshare-uts"
    ])
    assert has_unshare_all or has_individual_unshares, "The script does not unshare all required namespaces."

    # Check for the binary execution at the end
    binary_path = "/home/user/investigation/data_worker"
    assert binary_path in content, f"The script does not execute {binary_path}."

    # Basic check to ensure the binary is executed as the main command for bwrap
    # It should appear after bwrap and its arguments
    bwrap_index = content.find("bwrap")
    binary_index = content.find(binary_path, bwrap_index)
    assert binary_index > bwrap_index, "The binary is not passed as an argument to bwrap."