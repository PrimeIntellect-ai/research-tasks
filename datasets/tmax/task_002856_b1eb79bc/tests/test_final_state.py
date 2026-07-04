# test_final_state.py

import os
import json
import subprocess
import pytest

def test_forensics_report():
    report_path = "/home/user/forensics_report.json"
    assert os.path.exists(report_path), f"Forensics report is missing: {report_path}"
    assert os.path.isfile(report_path), f"Forensics report path is not a file: {report_path}"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Forensics report is not valid JSON: {report_path}")

    assert "attacker_ip" in report, "Report is missing 'attacker_ip' key."
    assert "transcription" in report, "Report is missing 'transcription' key."

    assert report["attacker_ip"] == "203.0.113.84", f"Incorrect attacker IP: {report['attacker_ip']}"

    transcription = report["transcription"].lower()
    assert "curl" in transcription and "bash" in transcription, f"Transcription does not appear to contain the malicious payload. Got: {transcription}"

def test_sanitizer_executable():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.exists(sanitizer_path), f"Sanitizer script is missing: {sanitizer_path}"
    assert os.path.isfile(sanitizer_path), f"Sanitizer path is not a file: {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer script is not executable: {sanitizer_path}"

def test_sanitizer_corpus():
    sanitizer_path = "/home/user/sanitizer"
    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])
    evil_files = sorted([os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    evil_failed = []

    for filepath in clean_files:
        try:
            result = subprocess.run([sanitizer_path, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "ALLOW":
                clean_failed.append(os.path.basename(filepath))
        except Exception as e:
            clean_failed.append(f"{os.path.basename(filepath)} (Error: {str(e)})")

    for filepath in evil_files:
        try:
            result = subprocess.run([sanitizer_path, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "BLOCK":
                evil_failed.append(os.path.basename(filepath))
        except Exception as e:
            evil_failed.append(f"{os.path.basename(filepath)} (Error: {str(e)})")

    error_messages = []
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    if error_messages:
        pytest.fail("Sanitizer corpus evaluation failed. " + " | ".join(error_messages))