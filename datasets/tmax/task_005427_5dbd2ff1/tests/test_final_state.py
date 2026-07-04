# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_report_txt_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"{report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {report_path}, found {len(lines)}."
    assert lines[0] == "target_uri", f"Line 1 of report.txt is incorrect. Expected 'target_uri', got '{lines[0]}'."
    assert lines[1] == "8492", f"Line 2 of report.txt is incorrect. Expected '8492', got '{lines[1]}'."
    assert lines[2] == "DarkOverlord_Node", f"Line 3 of report.txt is incorrect. Expected 'DarkOverlord_Node', got '{lines[2]}'."

def test_server_patched_exists_and_executable():
    binary_path = "/home/user/server_patched"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_server_c_patched_logic():
    src_path = "/home/user/server.c"
    assert os.path.isfile(src_path), f"{src_path} is missing."

    with open(src_path, "r") as f:
        content = f.read()

    # Check if the patched code contains basic checks for Open Redirect
    has_slash_check = "('/'" in content or '"/"' in content or "strncmp" in content or content.find("[0] == '/'") != -1 or "strchr" in content
    has_http_check = "http" in content
    has_home_default = "/home" in content

    assert has_slash_check or has_http_check or has_home_default, "The C source code does not appear to contain the required open redirect mitigation logic (checking for '/', 'http', or defaulting to '/home')."

def test_evidence_files_exist_and_permissions():
    evidence_dir = "/home/user/evidence"
    assert os.path.isdir(evidence_dir), f"Directory {evidence_dir} is missing. Did you extract the zip?"

    expected_files = ["root.pem", "intermediate.pem", "rogue.pem"]
    for file_name in expected_files:
        file_path = os.path.join(evidence_dir, file_name)
        assert os.path.isfile(file_path), f"Extracted file {file_path} is missing."

        st = os.stat(file_path)
        perms = stat.S_IMODE(st.st_mode)
        assert perms == 0o400, f"Permissions for {file_path} are incorrect. Expected 400 (read-only for owner), got {oct(perms)}."