# test_final_state.py
import os
import re
import pytest

def test_phase1_run_auth_sh():
    """Verify run_auth.sh passes password via environment variable, not CLI."""
    path = "/home/user/run_auth.sh"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "AUTH_SECRET" in content, f"File {path} must set or export the AUTH_SECRET environment variable."
    assert "--password" not in content, f"File {path} must NOT pass the password via the --password command-line argument."
    assert re.search(r"python3\s+/home/user/auth_service\.py\s+--user", content), f"File {path} must still call the python script with the --user argument."

def test_phase1_auth_service_py():
    """Verify auth_service.py reads the password from the environment."""
    path = "/home/user/auth_service.py"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert re.search(r"import\s+os\b", content), f"File {path} must import the 'os' module to read environment variables."
    assert re.search(r"os\.environ(?:\[['\"]AUTH_SECRET['\"]\]|\.get\(['\"]AUTH_SECRET['\"]\))", content), f"File {path} must read 'AUTH_SECRET' from os.environ."

def test_phase2_flagged_ips():
    """Verify the IDS monitor correctly identified and sorted the flagged IPs."""
    path = "/home/user/flagged_ips.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did the IDS script run and create it?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ips = ["172.16.0.2", "192.168.1.20"]
    assert lines == expected_ips, f"Contents of {path} are incorrect. Expected {expected_ips}, but got {lines}."

def test_phase3_sandbox_cmd():
    """Verify the bwrap sandbox command is constructed correctly."""
    path = "/home/user/sandbox_cmd.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    assert "bwrap" in content, f"Command in {path} must use the 'bwrap' executable."
    assert "--ro-bind / /" in content, f"Command in {path} must bind the root filesystem as read-only (--ro-bind / /)."
    assert "--dev /dev" in content, f"Command in {path} must mount devfs (--dev /dev)."
    assert "--proc /proc" in content, f"Command in {path} must mount procfs (--proc /proc)."
    assert "--tmpfs /tmp" in content, f"Command in {path} must create a tmpfs (--tmpfs /tmp)."
    assert "--unshare-all" in content, f"Command in {path} must isolate namespaces (--unshare-all)."

    assert re.search(r"python3\s+/home/user/auth_service\.py\s+--user\s+guest", content), f"Command in {path} must execute python3 /home/user/auth_service.py --user guest inside the sandbox."