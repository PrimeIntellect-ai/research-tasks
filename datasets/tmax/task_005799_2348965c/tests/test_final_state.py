# test_final_state.py

import os
import re
import stat
import hashlib
import subprocess
import pytest

def get_expected_cookie():
    dump_path = "/home/user/audit/http_traffic.dump"
    if not os.path.isfile(dump_path):
        return None
    with open(dump_path, "r") as f:
        for line in f:
            if line.lower().startswith("set-cookie:"):
                match = re.search(r"session=([^;]+)", line)
                if match:
                    return match.group(1)
    return None

def get_expected_log():
    checksum_path = "/home/user/audit/checksum.txt"
    logs_dir = "/home/user/audit/logs"
    if not os.path.isfile(checksum_path) or not os.path.isdir(logs_dir):
        return None

    with open(checksum_path, "r") as f:
        expected_hash = f.read().strip()

    for filename in os.listdir(logs_dir):
        filepath = os.path.join(logs_dir, filename)
        if os.path.isfile(filepath):
            with open(filepath, "rb") as lf:
                file_hash = hashlib.sha256(lf.read()).hexdigest()
            if file_hash == expected_hash:
                return filename
    return None

def test_report_exists():
    assert os.path.isfile("/home/user/audit_report.txt"), "The report file /home/user/audit_report.txt is missing."

def test_report_content():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), "The report file is missing."

    with open(report_path, "r") as f:
        content = f.read()

    expected_cookie = get_expected_cookie()
    assert expected_cookie is not None, "Could not compute expected cookie from dump."
    assert f"Cookie: {expected_cookie}" in content, "The Cookie line in the report is incorrect or missing."

    expected_log = get_expected_log()
    assert expected_log is not None, "Could not compute expected log file from checksum."
    assert f"Valid Log: {expected_log}" in content, "The Valid Log line in the report is incorrect or missing."

    assert "CWE: CWE-732" in content, "The CWE line in the report is incorrect or missing. Expected CWE-732."
    assert "Fixed: Yes" in content, "The Fixed line in the report is incorrect or missing."

def test_parser_fixed_executable():
    binary_path = "/home/user/audit/parser_fixed"
    assert os.path.isfile(binary_path), f"The fixed binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"The fixed binary {binary_path} is not executable."

def test_parser_fixed_permissions():
    binary_path = "/home/user/audit/parser_fixed"
    assert os.path.isfile(binary_path), f"The fixed binary {binary_path} is missing."

    test_out = "/home/user/audit/test_out_verify.txt"
    if os.path.exists(test_out):
        os.remove(test_out)

    try:
        subprocess.run([binary_path, test_out], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pytest.fail(f"Execution of {binary_path} failed.")

    assert os.path.isfile(test_out), f"The binary {binary_path} did not create the output file."

    st = os.stat(test_out)
    perms = stat.S_IMODE(st.st_mode)

    os.remove(test_out)

    assert perms == 0o600, f"The fixed binary created a file with incorrect permissions. Expected 0600, got {oct(perms)}."