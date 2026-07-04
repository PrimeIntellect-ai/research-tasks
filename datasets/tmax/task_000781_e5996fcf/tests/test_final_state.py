# test_final_state.py
import os
import json
import subprocess
from datetime import datetime

def test_policy_scanner_script_exists():
    script_path = "/home/user/policy_scanner.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_scan_report_exists_and_valid_json():
    report_path = "/home/user/scan_report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} was not created."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    assert isinstance(report, dict), "The root of the JSON report must be a dictionary."
    assert "violations" in report, "The JSON report is missing the 'violations' key."
    assert isinstance(report["violations"], list), "The 'violations' key must be a list."

def test_scan_report_correct_violations():
    # Re-evaluate the rules based on the actual files to be robust
    cert_path = "/home/user/cert.pem"
    headers_path = "/home/user/headers.json"

    expected_violations = []

    # Check TLS expiration and weak sig
    if os.path.isfile(cert_path):
        check_expired = subprocess.run(["openssl", "x509", "-in", cert_path, "-noout", "-checkend", "0"], capture_output=True)
        if check_expired.returncode != 0:
            expected_violations.append("TLS_EXPIRED")

        sig_result = subprocess.run(["openssl", "x509", "-in", cert_path, "-noout", "-text"], capture_output=True, text=True)
        if "sha1WithRSAEncryption" in sig_result.stdout or "md5WithRSAEncryption" in sig_result.stdout:
            expected_violations.append("TLS_WEAK_SIG")

    # Check CSP
    if os.path.isfile(headers_path):
        with open(headers_path, 'r') as f:
            headers = json.load(f)

        # Case-insensitive header lookup just in case
        csp_header = None
        for k, v in headers.items():
            if k.lower() == "content-security-policy":
                csp_header = v
                break

        if csp_header is None:
            expected_violations.append("CSP_MISSING")
        else:
            csp_lower = csp_header.lower()
            if "'unsafe-inline'" in csp_lower or "'unsafe-eval'" in csp_lower:
                expected_violations.append("CSP_UNSAFE")

    expected_violations.sort()

    # Now check the student's report
    report_path = "/home/user/scan_report.json"
    assert os.path.isfile(report_path), "Report file missing."

    with open(report_path, 'r') as f:
        report = json.load(f)

    actual_violations = sorted(report.get("violations", []))

    assert actual_violations == expected_violations, (
        f"Expected violations {expected_violations}, but got {actual_violations}. "
        "Ensure your script correctly identifies all violations according to the rules."
    )