# test_final_state.py

import os
import pytest

def test_breached_ips_content():
    breached_ips_path = "/home/user/breached_ips.txt"
    assert os.path.isfile(breached_ips_path), f"File {breached_ips_path} does not exist."

    with open(breached_ips_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ips = ["172.16.0.4", "192.168.1.10"]
    assert sorted(lines) == expected_ips, f"Expected {expected_ips} in {breached_ips_path}, but got {lines}."

def test_vulnerable_binaries_content():
    vuln_binaries_path = "/home/user/vulnerable_binaries.txt"
    assert os.path.isfile(vuln_binaries_path), f"File {vuln_binaries_path} does not exist."

    with open(vuln_binaries_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_binaries = ["vuln_echo"]
    assert sorted(lines) == expected_binaries, f"Expected {expected_binaries} in {vuln_binaries_path}, but got {lines}."

def test_run_sandbox_script():
    sandbox_script_path = "/home/user/run_sandbox.sh"
    assert os.path.isfile(sandbox_script_path), f"File {sandbox_script_path} does not exist."

    with open(sandbox_script_path, "r") as f:
        content = f.read()

    assert "bwrap" in content, "The run_sandbox.sh script does not invoke 'bwrap'."

    required_flags = [
        "--unshare-net",
        "--ro-bind /usr /usr",
        "--ro-bind /bin /bin",
        "--ro-bind /lib /lib",
        "--ro-bind /lib64 /lib64",
        "--rw-bind /home/user /home/user",
        "--dev /dev"
    ]

    # Normalize whitespace to safely check for arguments
    normalized_content = " ".join(content.split())

    for flag in required_flags:
        # Some flags have spaces, let's normalize them too
        normalized_flag = " ".join(flag.split())
        assert normalized_flag in normalized_content, f"Missing required bwrap flag/mount: '{flag}' in {sandbox_script_path}"