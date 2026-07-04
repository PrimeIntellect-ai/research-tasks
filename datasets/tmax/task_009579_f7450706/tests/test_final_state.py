# test_final_state.py

import os
import re
import hashlib
import urllib.parse
import pytest

def get_expected_critical_findings():
    log_file = "/home/user/service/logs/server.log"
    uploads_dir = "/home/user/service/uploads/"

    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    expected_paths = set()

    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Extract token and uploaded path
            match = re.search(r"Token:\s*(\S+)\s*-\s*UploadedPath:\s*(\S+)", line)
            if not match:
                continue

            token = match.group(1)
            raw_path = match.group(2)

            # Check for path traversal sequences
            if "../" not in raw_path and "..%2F" not in raw_path:
                continue

            # Validate token (sha256 hash starts with "00")
            token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
            if not token_hash.startswith("00"):
                continue

            # Resolve path
            unquoted_path = urllib.parse.unquote(raw_path)
            abs_path = os.path.normpath(os.path.join(uploads_dir, unquoted_path))

            # Check if file exists and is executable
            if os.path.isfile(abs_path) and os.access(abs_path, os.X_OK):
                expected_paths.add(abs_path)

    return expected_paths

def test_critical_findings_file():
    findings_file = "/home/user/critical_findings.txt"
    assert os.path.isfile(findings_file), f"The file {findings_file} does not exist. You need to create it."

    with open(findings_file, "r") as f:
        actual_paths = set(line.strip() for line in f if line.strip())

    expected_paths = get_expected_critical_findings()

    missing = expected_paths - actual_paths
    extra = actual_paths - expected_paths

    error_msg = []
    if missing:
        error_msg.append(f"Missing expected executable malicious paths: {', '.join(missing)}")
    if extra:
        error_msg.append(f"Included incorrect paths (not executable, invalid token, or safe): {', '.join(extra)}")

    assert not missing and not extra, " | ".join(error_msg)