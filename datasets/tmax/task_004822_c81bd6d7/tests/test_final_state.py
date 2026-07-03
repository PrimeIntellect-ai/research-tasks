# test_final_state.py

import os
import json
import subprocess
import tempfile
import glob

SCRIPT_PATH = "/home/user/audit_filter.py"
CLEAN_DIR = "/app/clean"
EVIL_DIR = "/app/evil"
SALT = "COMPLIANCE_v7_8923"

def process_file(input_file, output_file):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, input_file, output_file],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def compute_expected_evil(data):
    out = json.loads(json.dumps(data))

    # Rule 1: Sensitive Data Redaction
    if "payload" in out and isinstance(out["payload"], dict) and "password" in out["payload"]:
        pwd = out["payload"]["password"]
        if isinstance(pwd, str):
            is_hash = len(pwd) == 64 and all(c in "0123456789abcdef" for c in pwd)
            if not is_hash:
                out["payload"]["password"] = f"[REDACTED: {SALT}]"

    # Rule 2: Exploit Delivery Detection
    for section in ["payload", "headers"]:
        if section in out and isinstance(out[section], dict):
            for k, v in out[section].items():
                if isinstance(v, str):
                    v_lower = v.lower()
                    if "<script>" in v_lower or "${jndi:" in v_lower:
                        out[section][k] = "[EXPLOIT_BLOCKED]"

    # Rule 3: CSP Enforcement
    has_csp = False
    if "headers" in out and isinstance(out["headers"], dict) and "Content-Security-Policy" in out["headers"]:
        csp = out["headers"]["Content-Security-Policy"]
        if isinstance(csp, str) and "default-src 'self'" in csp:
            has_csp = True

    if not has_csp:
        out["COMPLIANCE_WARNING"] = "MISSING_CSP"

    return out

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.json"))
    assert len(clean_files) > 0, "No clean files found."

    modified_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for input_file in clean_files:
            basename = os.path.basename(input_file)
            output_file = os.path.join(tmpdir, basename)

            success = process_file(input_file, output_file)
            if not success or not os.path.exists(output_file):
                modified_files.append(basename)
                continue

            with open(input_file, "r") as f:
                in_data = json.load(f)
            with open(output_file, "r") as f:
                try:
                    out_data = json.load(f)
                except json.JSONDecodeError:
                    modified_files.append(basename)
                    continue

            if in_data != out_data:
                modified_files.append(basename)

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean files modified or failed: {', '.join(modified_files)}"

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.json"))
    assert len(evil_files) > 0, "No evil files found."

    bypassed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for input_file in evil_files:
            basename = os.path.basename(input_file)
            output_file = os.path.join(tmpdir, basename)

            success = process_file(input_file, output_file)
            if not success or not os.path.exists(output_file):
                bypassed_files.append(basename)
                continue

            with open(input_file, "r") as f:
                in_data = json.load(f)
            with open(output_file, "r") as f:
                try:
                    out_data = json.load(f)
                except json.JSONDecodeError:
                    bypassed_files.append(basename)
                    continue

            expected_data = compute_expected_evil(in_data)

            if out_data != expected_data:
                bypassed_files.append(basename)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed or failed: {', '.join(bypassed_files)}"