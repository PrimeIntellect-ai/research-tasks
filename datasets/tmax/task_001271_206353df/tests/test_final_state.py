# test_final_state.py

import os
import stat
import re
from collections import Counter
import pytest

def test_audit_report_exists_and_correct():
    report_path = "/home/user/audit_report.txt"
    auth_log_path = "/home/user/auth.log"
    webroot_path = "/home/user/webroot"

    assert os.path.isfile(report_path), f"Audit report file {report_path} is missing."

    # 1. Determine the expected IP address from auth.log
    assert os.path.isfile(auth_log_path), f"Log file {auth_log_path} is missing."
    ip_counter = Counter()
    ip_pattern = re.compile(r"Failed password.*from\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")

    with open(auth_log_path, "r") as f:
        for line in f:
            match = ip_pattern.search(line)
            if match:
                ip_counter[match.group(1)] += 1

    assert ip_counter, "No failed password attempts found in auth.log"
    expected_ip = ip_counter.most_common(1)[0][0]

    # 2. Determine the expected world-writable files
    assert os.path.isdir(webroot_path), f"Webroot directory {webroot_path} is missing."
    world_writable_files = []

    for root, dirs, files in os.walk(webroot_path):
        for file in files:
            file_path = os.path.join(root, file)
            st = os.stat(file_path)
            if bool(st.st_mode & stat.S_IWOTH):
                world_writable_files.append(file_path)

    world_writable_files.sort()

    # 3. Construct expected content
    expected_lines = [expected_ip] + world_writable_files
    expected_content = "\n".join(expected_lines) + "\n"

    # 4. Read actual content
    with open(report_path, "r") as f:
        actual_content = f.read()

    # Normalize newlines for comparison
    actual_lines = [line for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {report_path} is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )