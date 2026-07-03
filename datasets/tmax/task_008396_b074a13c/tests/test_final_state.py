# test_final_state.py

import os
import json
import subprocess

def test_incident_report_json():
    """Verify the incident report exists, is valid JSON, and contains correct values."""
    report_path = '/home/user/incident_report.json'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not valid JSON."

    assert "vulnerabilities" in report_data, "Report missing 'vulnerabilities' key."
    assert "sandboxing_library_used" in report_data, "Report missing 'sandboxing_library_used' key."

    vulns = report_data["vulnerabilities"]
    assert isinstance(vulns, list), "'vulnerabilities' must be a list."

    # Check for Weak PRNG CWE
    assert "CWE-338" in vulns or "CWE-332" in vulns, "Report missing correct CWE for Weak PRNG (CWE-338 or CWE-332)."

    # Check for Buffer Overflow CWE
    assert "CWE-120" in vulns, "Report missing correct CWE for Classic Buffer Overflow (CWE-120)."

    # Check sandboxing library
    assert report_data["sandboxing_library_used"] == "libseccomp", "Incorrect 'sandboxing_library_used' value."

def test_authd_binary_exists_and_linked():
    """Verify that the authd binary is built and dynamically linked to libseccomp."""
    binary_path = '/home/user/incident/authd'
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."

    # Check dynamic linking with ldd
    try:
        ldd_output = subprocess.check_output(['ldd', binary_path], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to run ldd on {binary_path}: {e.output}"

    assert "libseccomp" in ldd_output, f"Binary {binary_path} is not dynamically linked against libseccomp."

def test_authd_uses_seccomp_api():
    """Verify that the authd binary calls seccomp_init."""
    binary_path = '/home/user/incident/authd'
    try:
        readelf_output = subprocess.check_output(['readelf', '-s', binary_path], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to run readelf on {binary_path}: {e.output}"

    assert "seccomp_init" in readelf_output, "Binary does not appear to call seccomp_init."

def test_vulnerabilities_removed_from_source():
    """Verify that strcpy and srand have been removed from the source code."""
    source_path = '/home/user/incident/auth_server.cpp'
    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."

    with open(source_path, 'r') as f:
        content = f.read()

    assert "strcpy" not in content, "The buffer overflow vulnerability (strcpy) has not been completely removed."
    assert "srand" not in content, "The weak PRNG vulnerability (srand) has not been completely removed."