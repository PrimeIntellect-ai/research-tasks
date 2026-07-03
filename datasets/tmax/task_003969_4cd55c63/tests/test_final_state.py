# test_final_state.py

import os
import re

def test_debugging_report_exists():
    assert os.path.isfile("/home/user/debugging_report.txt"), "The file /home/user/debugging_report.txt does not exist."

def test_debugging_report_contents():
    report_path = "/home/user/debugging_report.txt"
    expected_commit_path = "/tmp/expected_bad_commit"

    assert os.path.isfile(report_path), "The file /home/user/debugging_report.txt does not exist."
    assert os.path.isfile(expected_commit_path), "The expected bad commit file is missing from the system."

    with open(expected_commit_path, "r") as f:
        expected_bad_commit = f.read().strip()

    expected_token = "secr3t_g1t_h1st0ry_992"

    with open(report_path, "r") as f:
        content = f.read()

    bad_commit_match = re.search(r"^BAD_COMMIT=(.+)$", content, re.MULTILINE)
    admin_token_match = re.search(r"^ADMIN_TOKEN=(.+)$", content, re.MULTILINE)

    assert bad_commit_match is not None, "BAD_COMMIT line is missing or incorrectly formatted in debugging_report.txt."
    assert admin_token_match is not None, "ADMIN_TOKEN line is missing or incorrectly formatted in debugging_report.txt."

    actual_bad_commit = bad_commit_match.group(1).strip()
    actual_admin_token = admin_token_match.group(1).strip()

    assert actual_bad_commit == expected_bad_commit, f"Incorrect BAD_COMMIT. Expected {expected_bad_commit}, got {actual_bad_commit}."
    assert actual_admin_token == expected_token, f"Incorrect ADMIN_TOKEN. Expected {expected_token}, got {actual_admin_token}."