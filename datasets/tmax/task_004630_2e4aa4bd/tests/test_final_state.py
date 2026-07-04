# test_final_state.py

import os
import json
import subprocess
import pytest

REPORT_PATH = "/home/user/audit_report.json"
FILTER_SCRIPT_PATH = "/home/user/filter.py"
EVIL_CORPUS_DIR = "/home/user/audit/traffic_corpus/evil/"
CLEAN_CORPUS_DIR = "/home/user/audit/traffic_corpus/clean/"

def test_audit_report_exists_and_valid():
    assert os.path.isfile(REPORT_PATH), f"Audit report missing at {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Audit report is not valid JSON")

    expected = {
        "backdoor_passphrase": "crimson_sunrise_42",
        "rogue_cert_file": "chain4.pem",
        "rogue_ssh_key_file": "id_ed25519_rogue.pub",
        "identified_cwe": "CWE-22"
    }

    for key, expected_val in expected.items():
        assert key in report, f"Missing key '{key}' in audit report"
        assert report[key] == expected_val, f"Incorrect value for '{key}'. Expected '{expected_val}', got '{report[key]}'"

def test_filter_script_exists():
    assert os.path.isfile(FILTER_SCRIPT_PATH), f"Filter script missing at {FILTER_SCRIPT_PATH}"

def test_filter_script_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "No files found in evil corpus"
    assert len(clean_files) > 0, "No files found in clean corpus"

    bypassed_evil = []
    modified_clean = []

    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", FILTER_SCRIPT_PATH, evil_file],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "REJECT":
            bypassed_evil.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        result = subprocess.run(
            ["python3", FILTER_SCRIPT_PATH, clean_file],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "ACCEPT":
            modified_clean.append(os.path.basename(clean_file))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))