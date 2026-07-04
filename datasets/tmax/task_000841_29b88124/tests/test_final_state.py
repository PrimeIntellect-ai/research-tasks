# test_final_state.py

import os
import stat
import pytest

def test_privesc_log():
    log_path = "/home/user/privesc.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Privilege escalation auditing failed."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert set(lines) == {"developer", "ci_runner"}, f"{log_path} does not contain the correct non-admin privileged roles. Found: {lines}"

def test_injection_log():
    log_path = "/home/user/injection.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Injection vulnerability analysis failed."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_path = "/home/user/vulnerable_app/db.go"
    assert expected_path in lines, f"{log_path} does not contain the expected file path {expected_path}."

def test_xss_log():
    log_path = "/home/user/xss.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. XSS vulnerability analysis failed."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_path = "/home/user/vulnerable_app/views/index.html"
    assert expected_path in lines, f"{log_path} does not contain the expected file path {expected_path}."

def test_secrets_clean():
    clean_path = "/home/user/secrets_clean.txt"
    assert os.path.isfile(clean_path), f"File {clean_path} does not exist. Sensitive data redaction failed."

    with open(clean_path, "r") as f:
        content = f.read()

    assert "AKIAIOSFODNN7EXAMPLE" not in content, "First AWS access key was not redacted."
    assert "AKIA1234567890ABCDEF" not in content, "Second AWS access key was not redacted."
    assert "AWS_ACCESS_KEY_ID=[REDACTED]" in content, "First AWS access key was not correctly replaced with [REDACTED]."
    assert "SomeOtherKey=[REDACTED]" in content, "Second AWS access key was not correctly replaced with [REDACTED]."
    assert "DatabaseURL=postgres://user:pass@localhost:5432/db" in content, "Non-sensitive data was improperly modified."
    assert "AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" in content, "AWS secret key was improperly modified."

def test_block_sh():
    script_path = "/home/user/block.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist. Firewall script generation failed."

    # Check permissions
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} does not have executable permissions set."

    with open(script_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"{script_path} is empty."
    assert lines[0] == "#!/bin/bash", f"{script_path} does not start with #!/bin/bash."

    expected_ips = ["192.168.1.50", "10.0.0.5", "203.0.113.42"]
    for ip in expected_ips:
        expected_rule = f"iptables -A INPUT -s {ip} -j DROP"
        assert expected_rule in lines, f"Missing expected iptables rule for IP {ip} in {script_path}."