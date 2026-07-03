# test_final_state.py

import os
import time
import pytest
import requests
import subprocess
import difflib

def test_nginx_proxy_and_evaluator():
    """
    Test that Nginx is listening on 8080, proxying to 9001,
    and the Bash API evaluates expressions correctly.
    """
    url = "http://127.0.0.1:8080/api/v1/check"
    payload = "15 * 3"

    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx reverse proxy at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "45", f"Expected evaluator to return '45', got {repr(response.text)}"

def test_audit_logger():
    """
    Test that the audit logger is running on 9002 and logging requests.
    We send a unique request through the proxy and check the log.
    """
    unique_payload = f"8 + {int(time.time() % 1000)}"
    url = "http://127.0.0.1:8080/api/v1/check"

    try:
        requests.post(url, data=unique_payload, timeout=5)
    except requests.exceptions.RequestException:
        pass # Handled by the other test

    time.sleep(0.5) # Give the background process time to write to the log

    audit_log_path = "/tmp/audit.log"
    assert os.path.exists(audit_log_path), f"Audit log not found at {audit_log_path}. Ensure the audit daemon is writing to it."

    with open(audit_log_path, "r") as f:
        logs = f.read()

    assert unique_payload in logs, f"Audit log does not contain the expected payload '{unique_payload}'. Log contents:\n{logs}"

def test_reconciliation_diff():
    """
    Test that the log reconciliation script produced the correct diff.
    """
    diff_out_path = "/home/user/workspace/diff.out"
    assert os.path.exists(diff_out_path), f"Diff output not found at {diff_out_path}"

    # Recompute the expected merged file
    with open("/app/logs/server_a.log", "r") as f:
        lines_a = f.readlines()
    with open("/app/logs/server_b.log", "r") as f:
        lines_b = f.readlines()

    merged = sorted(list(set(lines_a + lines_b)))

    with open("/app/logs/baseline.log", "r") as f:
        baseline = f.readlines()

    # We don't enforce exact diff headers, but we check for the correct line additions/removals
    with open(diff_out_path, "r") as f:
        actual_diff = f.read()

    # The merged list should lack the unknown IP from baseline, and have different ordering for .5 vs .10
    # Let's just check that the actual diff contains the expected content markers.
    assert "-192.168.1.20 - GET /unknown" in actual_diff or "+192.168.1.20 - GET /unknown" in actual_diff, \
        "Diff output does not show the difference for '192.168.1.20 - GET /unknown'."

    assert "192.168.1.10" in actual_diff, "Diff output does not contain expected changes for 192.168.1.10."