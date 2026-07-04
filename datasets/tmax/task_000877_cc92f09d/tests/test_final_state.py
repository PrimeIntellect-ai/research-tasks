# test_final_state.py

import os
import stat
import json
import urllib.request
import pytest

def get_expected_files(base_dir):
    suid_files = []
    world_writable_files = []

    if os.path.isdir(base_dir):
        for root, _, files in os.walk(base_dir):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    st = os.stat(filepath)
                    mode = st.st_mode
                    if mode & stat.S_ISUID:
                        suid_files.append(filepath)
                    if mode & stat.S_IWOTH:
                        world_writable_files.append(filepath)
                except OSError:
                    pass

    return sorted(suid_files), sorted(world_writable_files)

def check_csp(url):
    try:
        response = urllib.request.urlopen(url, timeout=5)
        csp = response.headers.get('Content-Security-Policy')
        return bool(csp and csp.strip())
    except Exception:
        return False

def test_audit_go_exists():
    assert os.path.isfile("/home/user/audit.go"), "/home/user/audit.go does not exist."

def test_report_json_correct():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"{report_path} does not exist. Did you run your Go program?"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not a valid JSON file.")

    expected_suid, expected_ww = get_expected_files("/home/user/app")
    expected_csp = check_csp("http://localhost:8080/")

    assert "suid_files" in report, "Missing 'suid_files' key in report.json"
    assert "world_writable_files" in report, "Missing 'world_writable_files' key in report.json"
    assert "csp_enforced" in report, "Missing 'csp_enforced' key in report.json"

    assert isinstance(report["suid_files"], list), "'suid_files' must be a list"
    assert isinstance(report["world_writable_files"], list), "'world_writable_files' must be a list"
    assert isinstance(report["csp_enforced"], bool), "'csp_enforced' must be a boolean"

    assert sorted(report["suid_files"]) == expected_suid, f"Expected suid_files to be {expected_suid}, got {sorted(report['suid_files'])}"
    assert sorted(report["world_writable_files"]) == expected_ww, f"Expected world_writable_files to be {expected_ww}, got {sorted(report['world_writable_files'])}"
    assert report["csp_enforced"] == expected_csp, f"Expected csp_enforced to be {expected_csp}, got {report['csp_enforced']}"