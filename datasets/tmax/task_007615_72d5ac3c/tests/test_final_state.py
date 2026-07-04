# test_final_state.py

import os
import re
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        content = f.read()

    assert "CWE-78" in content, "CWE-78 (OS Command Injection) is missing from the audit report."
    assert "CWE-79" in content, "CWE-79 (Cross-Site Scripting) is missing from the audit report."

def test_source_code_fixed_command_injection():
    main_rs_path = "/home/user/traffic_dashboard/src/main.rs"
    assert os.path.isfile(main_rs_path), f"Source file not found at {main_rs_path}"

    with open(main_rs_path, "r") as f:
        content = f.read()

    # Check that 'sh' is no longer used to invoke grep
    # We look for common patterns of the vulnerable code
    assert not re.search(r'Command::new\(\s*"sh"\s*\)', content), "Source code still contains Command::new(\"sh\"), indicating the command injection vulnerability is not properly fixed."

def test_report_html_csp():
    report_path = "/home/user/report.html"
    assert os.path.isfile(report_path), f"Generated report not found at {report_path}"

    with open(report_path, "r") as f:
        content = f.read()

    # Check for CSP meta tag
    csp_pattern1 = r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content=["\']default-src\s+\'self\';["\']\s*/?>'
    csp_pattern2 = r'<meta\s+content=["\']default-src\s+\'self\';["\']\s+http-equiv=["\']Content-Security-Policy["\']\s*/?>'

    has_csp = re.search(csp_pattern1, content, re.IGNORECASE) or re.search(csp_pattern2, content, re.IGNORECASE)
    assert has_csp, "The generated HTML report does not contain the required Content-Security-Policy meta tag."

def test_report_html_xss_escaped():
    report_path = "/home/user/report.html"
    assert os.path.isfile(report_path), f"Generated report not found at {report_path}"

    with open(report_path, "r") as f:
        content = f.read()

    # Check that unescaped malicious payload is not present
    assert "<script>alert(1)</script>" not in content, "The generated HTML report contains unescaped malicious HTML tags (XSS vulnerability is still present)."

    # Check that the escaped version is present
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in content, "The malicious payload was not properly HTML-escaped in the generated report."