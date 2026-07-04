# test_final_state.py
import os
import stat
import re

def test_query_template_extracted():
    report_file = "/home/user/pentest_target/report/query_template.txt"
    assert os.path.isfile(report_file), f"Expected file {report_file} does not exist."

    with open(report_file, "r") as f:
        content = f.read().strip()

    expected_query = "SELECT * FROM users WHERE username='%s' AND password='%s'"
    assert content == expected_query, f"Extracted query is incorrect. Expected: {expected_query}, Got: {content}"

def test_attacker_logs_redacted():
    log_file = "/home/user/pentest_target/logs/access.log"
    report_file = "/home/user/pentest_target/report/attacker_logs_redacted.txt"

    assert os.path.isfile(log_file), f"Original log file {log_file} is missing."
    assert os.path.isfile(report_file), f"Expected report file {report_file} does not exist."

    # Derive expected redacted logs from the original access.log
    expected_lines = []
    with open(log_file, "r") as f:
        for line in f:
            if "admin'%20OR%20'1'%3D'1" in line and " 200 " in line:
                # Replace SessionID value with REDACTED
                redacted_line = re.sub(r"SessionID=[^&\s]+", "SessionID=REDACTED", line)
                expected_lines.append(redacted_line.strip())

    with open(report_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in redacted logs, got {len(actual_lines)}."

    for expected, actual in zip(expected_lines, actual_lines):
        assert expected == actual, f"Log line mismatch.\nExpected: {expected}\nGot:      {actual}"

def test_binary_permissions():
    binary_path = "/home/user/pentest_target/cgi-bin/process_login"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist."

    st = os.stat(binary_path)
    perms = stat.S_IMODE(st.st_mode)

    assert perms == 0o700, f"Permissions for {binary_path} are incorrect. Expected 700, got {oct(perms)[2:]}"