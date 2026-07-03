# test_final_state.py

import os
import json
import time
import subprocess
import pytest
import hashlib

def test_investigation_report_exists_and_correct():
    report_path = "/home/user/investigation_report.json"
    assert os.path.isfile(report_path), f"Missing investigation report at {report_path}"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Investigation report is not valid JSON")

    expected_password = "OmegaUpload7391"
    expected_endpoint = "/api/v2/internal/sys_upload_traversal_unsafe"
    expected_cn = "EvilCorp Intermediate CA G2"

    assert report.get("cracked_password") == expected_password, f"Incorrect cracked_password. Expected {expected_password}, got {report.get('cracked_password')}"
    assert report.get("vulnerable_endpoint") == expected_endpoint, f"Incorrect vulnerable_endpoint. Expected {expected_endpoint}, got {report.get('vulnerable_endpoint')}"
    assert report.get("invalid_cert_cn") == expected_cn, f"Incorrect invalid_cert_cn. Expected '{expected_cn}', got '{report.get('invalid_cert_cn')}'"

def test_fast_cracker_performance_and_accuracy():
    fast_cracker_path = "/home/user/fast_cracker"
    slow_cracker_path = "/app/slow_cracker.py"
    hash_file_path = "/app/target_hash.txt"

    assert os.path.isfile(fast_cracker_path), f"Missing fast_cracker at {fast_cracker_path}"
    assert os.access(fast_cracker_path, os.X_OK), f"fast_cracker at {fast_cracker_path} is not executable"

    if os.path.isfile(hash_file_path):
        with open(hash_file_path, "r") as f:
            target_hash = f.read().strip()
    else:
        # Fallback if file is somehow missing but we know the expected password
        target_hash = hashlib.sha256(b"OmegaUpload7391").hexdigest()

    # Run slow cracker
    start_slow = time.time()
    subprocess.run(["python3", slow_cracker_path, target_hash], capture_output=True)
    slow_time = time.time() - start_slow

    # Run fast cracker
    start_fast = time.time()
    fast_res = subprocess.run([fast_cracker_path, target_hash], capture_output=True, text=True)
    fast_time = time.time() - start_fast

    speedup = slow_time / fast_time if fast_time > 0 else float('inf')

    assert "OmegaUpload7391" in fast_res.stdout, f"Fast cracker did not output the correct password. Output: {fast_res.stdout}"
    assert speedup >= 25.0, f"Speedup {speedup:.2f}x is below the 25.0x threshold (Slow: {slow_time:.4f}s, Fast: {fast_time:.4f}s)"