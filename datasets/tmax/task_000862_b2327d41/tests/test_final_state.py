# test_final_state.py
import os
import json
import subprocess
import pytest

REPORT_PATH = "/home/user/security_report.json"
MAIN_RS_PATH = "/home/user/rogue_service/src/main.rs"
CARGO_TOML_PATH = "/home/user/rogue_service/Cargo.toml"

def test_security_report_exists_and_valid():
    assert os.path.isfile(REPORT_PATH), f"Security report not found at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert "discovered_port" in report, "Missing 'discovered_port' in report."
    assert report["discovered_port"] == 8123, f"Incorrect discovered_port. Expected 8123, got {report['discovered_port']}."

    assert "vulnerabilities" in report, "Missing 'vulnerabilities' in report."
    vulns = report["vulnerabilities"]
    assert isinstance(vulns, list), "'vulnerabilities' must be a list."
    assert "CWE-77" in vulns, "Missing CWE-77 (Command Injection) in vulnerabilities."
    assert "CWE-79" in vulns, "Missing CWE-79 (XSS) in vulnerabilities."

    assert "csp_header_added" in report, "Missing 'csp_header_added' in report."
    csp_val = report["csp_header_added"].strip()
    assert csp_val in ["default-src 'self'", "Content-Security-Policy: default-src 'self'"], \
        f"Incorrect csp_header_added value. Got: {csp_val}"

def test_main_rs_fixes_applied():
    assert os.path.isfile(MAIN_RS_PATH), f"Source file not found at {MAIN_RS_PATH}"

    with open(MAIN_RS_PATH, 'r') as f:
        content = f.read()

    # Check for CSP header
    assert "Content-Security-Policy: default-src 'self'" in content, \
        "The required Content-Security-Policy header was not found in the HTTP response."

    # Check that the shell interpreter usage is removed
    assert 'Command::new("sh")' not in content or '".arg("-c")' not in content.replace(" ", "").replace("\n", ""), \
        "The Command Injection vulnerability using `sh -c` is still present."

def test_cargo_check_succeeds():
    assert os.path.isfile(CARGO_TOML_PATH), f"Cargo.toml not found at {CARGO_TOML_PATH}"

    result = subprocess.run(
        ["cargo", "check", "--manifest-path", CARGO_TOML_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cargo check failed with exit code {result.returncode}.\nStderr: {result.stderr}"