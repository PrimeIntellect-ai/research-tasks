# test_final_state.py

import os
import stat
import json
import pytest

def test_libseccheck_exists():
    path = "/home/user/ffi/libseccheck.so"
    assert os.path.isfile(path), f"Shared library {path} is missing. Did you compile sec_check.c?"

def test_audit_sh_exists_and_executable():
    path = "/home/user/audit.sh"
    assert os.path.isfile(path), f"Bash script {path} is missing."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {path} is not executable. Run chmod +x on it."

def test_vuln_log_contents():
    path = "/home/user/vuln.log"
    assert os.path.isfile(path), f"Log file {path} is missing. Did your script generate it?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["auth-utils@1.2.0", "form-parser@0.9.4"]
    assert lines == expected, (
        f"Contents of {path} do not match the expected output. "
        f"Expected {expected}, but got {lines}. Ensure you only process [Web-Components] "
        "and sort the results alphabetically."
    )

def test_resolved_package_json():
    path = "/home/user/project/resolved_package.json"
    assert os.path.isfile(path), f"Resolved package file {path} is missing."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not a valid JSON file.")

    deps = data.get("dependencies", {})
    assert deps.get("express-router") == "4.5.0", (
        "The 'express-router' dependency in resolved_package.json was not updated to '4.5.0'."
    )