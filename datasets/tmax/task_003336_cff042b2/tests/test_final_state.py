# test_final_state.py
import os
import subprocess
import pytest

def test_c_file_exists():
    path = "/home/user/sec_audit.c"
    assert os.path.isfile(path), f"Source file {path} does not exist."

def test_executable_exists_and_runs():
    c_file = "/home/user/sec_audit.c"
    exe_file = "/home/user/sec_audit"

    # Compile if not already compiled
    if not os.path.isfile(exe_file) and os.path.isfile(c_file):
        subprocess.run(["gcc", c_file, "-o", exe_file], capture_output=True)

    assert os.path.isfile(exe_file), f"Executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

    # Run the executable to generate the report
    result = subprocess.run([exe_file], capture_output=True, cwd="/home/user")
    assert result.returncode == 0, f"Execution of {exe_file} failed with return code {result.returncode}."

def test_audit_report_content():
    report_file = "/home/user/audit_report.txt"
    assert os.path.isfile(report_file), f"Report file {report_file} was not created."

    with open(report_file, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) >= 3, f"Report file {report_file} does not contain the expected number of lines."

    ssh_hardened_found = False
    cert_valid_found = False
    malicious_ips_found = False

    for line in content:
        line = line.strip()
        if line.startswith("SSH_HARDENED:"):
            assert line == "SSH_HARDENED: NO", f"Expected 'SSH_HARDENED: NO', got '{line}'"
            ssh_hardened_found = True
        elif line.startswith("CERT_VALID:"):
            assert line == "CERT_VALID: YES", f"Expected 'CERT_VALID: YES', got '{line}'"
            cert_valid_found = True
        elif line.startswith("MALICIOUS_IPS:"):
            expected_ips = "10.9.8.7, 172.16.5.5"
            assert line == f"MALICIOUS_IPS: {expected_ips}", f"Expected 'MALICIOUS_IPS: {expected_ips}', got '{line}'"
            malicious_ips_found = True

    assert ssh_hardened_found, "SSH_HARDENED check missing from report."
    assert cert_valid_found, "CERT_VALID check missing from report."
    assert malicious_ips_found, "MALICIOUS_IPS check missing from report."