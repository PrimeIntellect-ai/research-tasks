# test_final_state.py
import os
import stat
import pytest

def test_mitigation_directory_exists():
    """Test that the mitigation directory was created."""
    assert os.path.isdir("/home/user/mitigation"), "/home/user/mitigation directory is missing"

def test_payloads_file_content_and_permissions():
    """Test payloads.txt content and permissions."""
    payloads_file = "/home/user/mitigation/payloads.txt"
    assert os.path.isfile(payloads_file), f"{payloads_file} is missing"

    # Check permissions
    st = os.stat(payloads_file)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Permissions for {payloads_file} are {oct(permissions)}, expected 0o400"

    # Check content
    with open(payloads_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_payloads = {
        "<script>fetch('http://evil-corp.com')</script>",
        "ls; cat /etc/passwd",
        "<script>alert(1)</script>"
    }

    assert set(lines) == expected_payloads, f"Content of {payloads_file} does not match expected unique malicious payloads"

def test_block_ips_script_content():
    """Test block_ips.sh content."""
    script_file = "/home/user/mitigation/block_ips.sh"
    assert os.path.isfile(script_file), f"{script_file} is missing"

    with open(script_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_rules = {
        "ufw deny from 192.168.1.105",
        "ufw deny from 10.0.0.55"
    }

    assert set(lines) == expected_rules, f"Content of {script_file} does not match expected firewall rules"

def test_csp_txt_content():
    """Test csp.txt content."""
    csp_file = "/home/user/mitigation/csp.txt"
    assert os.path.isfile(csp_file), f"{csp_file} is missing"

    with open(csp_file, "r") as f:
        content = f.read().strip()

    expected_csp = "default-src 'self'; script-src 'self';"
    assert content == expected_csp, f"Content of {csp_file} is incorrect"

def test_analyze_go_exists():
    """Test that the analyze.go program exists."""
    assert os.path.isfile("/home/user/analyze.go"), "/home/user/analyze.go is missing"