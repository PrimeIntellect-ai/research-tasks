# test_final_state.py
import os
import re

def test_recover_go_exists():
    assert os.path.isfile("/home/user/recover.go"), "/home/user/recover.go does not exist."

def test_recovered_evidence():
    evidence_path = "/home/user/recovered_evidence.txt"
    assert os.path.isfile(evidence_path), f"File {evidence_path} does not exist."

    with open(evidence_path, "r") as f:
        content = f.read().strip()

    expected_content = 'EVIDENCE_DATA:{user:"admin_root",stolen_hash:"f8b9a1c2d3e4f5a6b7c8d9e0f1a2b3c4"}'
    assert expected_content in content, f"The decrypted evidence is incorrect. Found: {content}"

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().upper()

    # Look for CWE-22 and CWE-327
    has_cwe_22 = "CWE-22" in content
    has_cwe_327 = "CWE-327" in content

    assert has_cwe_22 and has_cwe_327, f"The audit report must contain both CWE-22 and CWE-327. Content found: {content}"