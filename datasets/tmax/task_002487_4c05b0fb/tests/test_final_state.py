# test_final_state.py

import os
import subprocess
import hashlib
import pytest
import shutil

def run_test(args, expected_code, expected_stderr=""):
    try:
        res = subprocess.run(["/home/user/secure_wrapper"] + args, capture_output=True, text=True, timeout=2)
        if res.returncode == expected_code and expected_stderr in res.stderr:
            return 1
        return 0
    except Exception:
        return 0

def test_secure_wrapper_accuracy():
    wrapper_path = "/home/user/secure_wrapper"
    assert os.path.exists(wrapper_path), f"Wrapper binary not found at {wrapper_path}"
    assert os.access(wrapper_path, os.X_OK), f"Wrapper binary at {wrapper_path} is not executable"

    tests_passed = 0
    total_tests = 5

    # Setup test environment
    os.makedirs('/app/data/in', exist_ok=True)
    os.makedirs('/app/data/out', exist_ok=True)
    os.makedirs('/tmp/malicious', exist_ok=True)

    # Test 1: Path violation (input)
    if run_test(["/tmp/malicious/in.txt", "/app/data/out/out.txt"], 1, "POLICY_VIOLATION"):
        tests_passed += 1

    # Test 2: Path violation (output)
    if run_test(["/app/data/in/in.txt", "/tmp/malicious/out.txt"], 1, "POLICY_VIOLATION"):
        tests_passed += 1

    # Test 3: Integrity violation
    with open("/app/data/in/bad.txt", "w") as f: 
        f.write("bad")
    with open("/app/data/in/bad.txt.sha256", "w") as f: 
        f.write("0"*64 + "\n")
    if run_test(["/app/data/in/bad.txt", "/app/data/out/out.txt"], 2, "INTEGRITY_ERROR"):
        tests_passed += 1

    # Test 4: Integrity passing but parser fails gracefully
    content = b"good data"
    with open("/app/data/in/good.txt", "wb") as f: 
        f.write(content)
    with open("/app/data/in/good.txt.sha256", "w") as f: 
        f.write(hashlib.sha256(content).hexdigest() + "\n")

    res = subprocess.run(["/home/user/secure_wrapper", "/app/data/in/good.txt", "/app/data/out/out.txt"], capture_output=True, text=True)
    if "POLICY_VIOLATION" not in res.stderr and "INTEGRITY_ERROR" not in res.stderr:
        tests_passed += 1

    # Test 5: Check if seccomp is applied
    with open("/app/data/in/dummy.txt", "wb") as f: 
        f.write(b"dummy")
    with open("/app/data/in/dummy.txt.sha256", "w") as f: 
        f.write(hashlib.sha256(b"dummy").hexdigest() + "\n")

    backup_parser = "/app/bin/data_parser_bak"
    shutil.move("/app/bin/data_parser", backup_parser)
    try:
        with open("/app/bin/data_parser", "w") as f:
            f.write("#!/bin/bash\npython3 -c 'import socket; s=socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.bind((\"127.0.0.1\", 0))'\nexit $?\n")
        os.chmod("/app/bin/data_parser", 0o755)

        res = subprocess.run(["/home/user/secure_wrapper", "/app/data/in/dummy.txt", "/app/data/out/out.txt"], capture_output=True)
        if res.returncode != 0:
            tests_passed += 1
    finally:
        shutil.move(backup_parser, "/app/bin/data_parser")

    accuracy = tests_passed / total_tests
    assert accuracy >= 1.0, f"Accuracy metric failed. Expected >= 1.0, got {accuracy} ({tests_passed}/{total_tests} tests passed)"