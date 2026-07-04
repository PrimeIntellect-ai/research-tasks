# test_final_state.py

import os
import json
import hashlib
import pytest

REPORT_PATH = "/home/user/audit_report.json"
LOG_PATH = "/home/user/audit_data/server.log"
UPLOADS_DIR = "/home/user/audit_data/uploads/"

def get_expected_state():
    assert os.path.isfile(LOG_PATH), f"Log file missing: {LOG_PATH}"

    flagged_requests = []
    compromised_sessions = []
    traversed_files_hashes = {}

    with open(LOG_PATH, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)

            req_id = record.get("req_id")
            endpoint = record.get("endpoint")
            headers = record.get("headers", {})
            resp_headers = record.get("resp_headers", {})
            file_saved_path = record.get("file_saved_path")

            is_flagged = False
            is_traversal = False

            # 1. CSP Enforcement Check
            if endpoint == "/upload":
                csp = resp_headers.get("Content-Security-Policy")
                if csp != "default-src 'self'":
                    is_flagged = True

            # 2. Path Traversal Identification
            if file_saved_path:
                # Resolve absolute path to be sure
                abs_saved_path = os.path.abspath(file_saved_path)
                abs_uploads_dir = os.path.abspath(UPLOADS_DIR)

                # Check if it's outside the uploads directory
                if not abs_saved_path.startswith(abs_uploads_dir + os.sep):
                    is_flagged = True
                    is_traversal = True

            if is_flagged:
                flagged_requests.append(req_id)

                # Extract session ID
                cookie = headers.get("Cookie", "")
                session_id = None
                for part in cookie.split(";"):
                    part = part.strip()
                    if part.startswith("session_id="):
                        session_id = part.split("=")[1]
                        break

                if session_id:
                    compromised_sessions.append(session_id)

                # File Integrity Verification
                if is_traversal and file_saved_path:
                    if os.path.isfile(file_saved_path):
                        with open(file_saved_path, 'rb') as tf:
                            file_hash = hashlib.sha256(tf.read()).hexdigest()
                        traversed_files_hashes[file_saved_path] = file_hash

    return {
        "flagged_requests": sorted(flagged_requests),
        "compromised_sessions": sorted(compromised_sessions),
        "traversed_files_hashes": traversed_files_hashes
    }

def test_audit_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Audit report not found at {REPORT_PATH}"

def test_audit_report_content():
    assert os.path.isfile(REPORT_PATH), f"Audit report not found at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Audit report at {REPORT_PATH} is not valid JSON")

    expected = get_expected_state()

    # 1. Check flagged requests
    actual_flagged = report.get("flagged_requests")
    assert actual_flagged is not None, "Missing 'flagged_requests' in report"
    assert isinstance(actual_flagged, list), "'flagged_requests' must be a list"
    assert sorted(actual_flagged) == expected["flagged_requests"], \
        f"Flagged requests mismatch. Expected {expected['flagged_requests']}, got {sorted(actual_flagged)}"

    # 2. Check compromised sessions
    actual_sessions = report.get("compromised_sessions")
    assert actual_sessions is not None, "Missing 'compromised_sessions' in report"
    assert isinstance(actual_sessions, list), "'compromised_sessions' must be a list"
    assert sorted(actual_sessions) == expected["compromised_sessions"], \
        f"Compromised sessions mismatch. Expected {expected['compromised_sessions']}, got {sorted(actual_sessions)}"

    # 3. Check traversed files hashes
    actual_hashes = report.get("traversed_files_hashes")
    assert actual_hashes is not None, "Missing 'traversed_files_hashes' in report"
    assert isinstance(actual_hashes, dict), "'traversed_files_hashes' must be an object/dict"
    assert actual_hashes == expected["traversed_files_hashes"], \
        f"Traversed files hashes mismatch. Expected {expected['traversed_files_hashes']}, got {actual_hashes}"