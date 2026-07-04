# test_final_state.py
import os
import re

def test_summary_log_exists():
    assert os.path.isfile("/home/user/backups/summary.log"), "The file /home/user/backups/summary.log does not exist."

def test_go_script_exists():
    assert os.path.isfile("/home/user/process_logs.go"), "The Go script /home/user/process_logs.go does not exist."

def test_extracted_files_exist():
    extracted_dir = "/home/user/backups/extracted"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."

    # Check that the log files were successfully extracted from the hidden archives
    log_files = ["app1.log", "hidden.log", "regular.log"]
    for lf in log_files:
        path = os.path.join(extracted_dir, lf)
        assert os.path.isfile(path), f"Expected extracted file {path} is missing. Did you correctly identify and extract the hidden archives?"

def test_summary_log_contents():
    summary_path = "/home/user/backups/summary.log"
    with open(summary_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify that specific redacted lines exist
    expected_lines = [
        "Host: [REDACTED]",
        "Client IP: [REDACTED]",
        "Timeout reaching [REDACTED]"
    ]
    for line in expected_lines:
        assert line in content, f"Expected redacted line '{line}' not found in summary.log."

    # Verify that no IPv4 addresses remain in the file
    ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    found_ips = ipv4_pattern.findall(content)
    assert not found_ips, f"Found unredacted IPv4 addresses in summary.log: {found_ips}"

    # Verify that error blocks start with [ERROR]
    assert "[ERROR]" in content, "No [ERROR] blocks found in summary.log."