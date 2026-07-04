# test_final_state.py
import os

def test_audit_report_exists():
    path = "/home/user/audit_report.txt"
    assert os.path.isfile(path), f"Missing audit report: {path}"

def test_audit_report_contents():
    path = "/home/user/audit_report.txt"
    with open(path, "r") as f:
        content = f.read()

    report = {}
    for line in content.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            report[key.strip()] = val.strip()

    assert "RECOVERED_KEY" in report, "Missing RECOVERED_KEY in audit report"
    assert "5a5a" in report["RECOVERED_KEY"].lower(), f"Incorrect RECOVERED_KEY: {report['RECOVERED_KEY']}"

    assert "ADMIN_TOKEN_PLAINTEXT" in report, "Missing ADMIN_TOKEN_PLAINTEXT in audit report"
    admin_token = report["ADMIN_TOKEN_PLAINTEXT"].lower()
    assert "dead" in admin_token or "57005" in admin_token, f"Incorrect ADMIN_TOKEN_PLAINTEXT: {report['ADMIN_TOKEN_PLAINTEXT']}"

    assert "FLAG" in report, "Missing FLAG in audit report"
    assert "FLAG{c_sec_aud1t_pwn}" in report["FLAG"], f"Incorrect FLAG: {report['FLAG']}"