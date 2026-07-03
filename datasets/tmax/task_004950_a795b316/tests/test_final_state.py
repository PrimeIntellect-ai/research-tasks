# test_final_state.py

import os
import json
import base64
import hashlib
import pytest

REPORT_PATH = "/home/user/report.json"
PROC_DUMP_DIR = "/home/user/proc_dump"
HASHES_PATH = "/home/user/hashes.txt"

def get_authorized_hashes():
    hashes = set()
    if os.path.exists(HASHES_PATH):
        with open(HASHES_PATH, "r") as f:
            for line in f:
                h = line.strip()
                if h:
                    hashes.add(h)
    return hashes

def compute_expected_findings():
    authorized_hashes = get_authorized_hashes()
    expected_findings = []

    if not os.path.isdir(PROC_DUMP_DIR):
        return expected_findings

    for pid_str in os.listdir(PROC_DUMP_DIR):
        if not pid_str.isdigit():
            continue

        pid = int(pid_str)
        pid_dir = os.path.join(PROC_DUMP_DIR, pid_str)

        # Check integrity
        exe_path = os.path.join(pid_dir, "exe")
        integrity_valid = False
        if os.path.isfile(exe_path):
            with open(exe_path, "rb") as f:
                exe_data = f.read()
                exe_hash = hashlib.sha256(exe_data).hexdigest()
                if exe_hash in authorized_hashes:
                    integrity_valid = True

        # Extract and redact token
        cmdline_path = os.path.join(pid_dir, "cmdline")
        redacted_token = ""
        if os.path.isfile(cmdline_path):
            with open(cmdline_path, "rb") as f:
                cmdline_data = f.read()

            args = cmdline_data.split(b'\0')
            for arg in args:
                if arg.startswith(b'--token='):
                    b64_token = arg[8:]
                    try:
                        decoded = base64.b64decode(b64_token).decode('utf-8')
                        if len(decoded) > 2:
                            redacted_token = decoded[:2] + '*' * (len(decoded) - 2)
                        else:
                            redacted_token = decoded[:2]
                    except Exception:
                        pass
                    break

        expected_findings.append({
            "pid": pid,
            "redacted_token": redacted_token,
            "integrity_valid": integrity_valid
        })

    expected_findings.sort(key=lambda x: x["pid"])
    return expected_findings

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

def test_report_json_format():
    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Report is not valid JSON.")

    assert isinstance(data, dict), "Report JSON must be an object."
    assert "csp_policy" in data, "Missing 'csp_policy' key in report."
    assert "findings" in data, "Missing 'findings' key in report."

def test_csp_policy():
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert data.get("csp_policy") == "default-src 'none';", "Incorrect csp_policy value."

def test_findings_content():
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    actual_findings = data.get("findings", [])
    expected_findings = compute_expected_findings()

    assert len(actual_findings) == len(expected_findings), \
        f"Expected {len(expected_findings)} findings, got {len(actual_findings)}."

    # Ensure they are sorted by pid
    pids = [f.get("pid") for f in actual_findings]
    assert pids == sorted(pids), "Findings are not sorted by pid in ascending order."

    for expected, actual in zip(expected_findings, actual_findings):
        assert actual.get("pid") == expected["pid"], \
            f"PID mismatch: expected {expected['pid']}, got {actual.get('pid')}"
        assert actual.get("redacted_token") == expected["redacted_token"], \
            f"Redacted token mismatch for PID {expected['pid']}: expected '{expected['redacted_token']}', got '{actual.get('redacted_token')}'"
        assert actual.get("integrity_valid") == expected["integrity_valid"], \
            f"Integrity valid mismatch for PID {expected['pid']}: expected {expected['integrity_valid']}, got {actual.get('integrity_valid')}"