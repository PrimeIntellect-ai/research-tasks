# test_final_state.py

import os
import subprocess
import hashlib
import pytest

def test_patched_upload_program():
    patched_file = "/home/user/src/upload_patched.c"
    assert os.path.isfile(patched_file), f"Patched file {patched_file} not found. The service must be patched and saved to this path."

    # Compile the patched C code
    exe_path = "/tmp/upload_patched"
    compile_res = subprocess.run(["gcc", patched_file, "-o", exe_path], capture_output=True, text=True)
    assert compile_res.returncode == 0, f"Compilation of {patched_file} failed:\n{compile_res.stderr}"

    # Re-derive the expected token based on the truth data
    extracted_text = "R0t4t10n_K3y_2024"
    old_token = "OLD_c0mpr0m1s3d_t0k3n"
    expected_token = hashlib.sha256(f"{extracted_text}:{old_token}".encode()).hexdigest()

    # Define the test suite (50 requests: 25 benign, 25 malicious)
    benign_files = [f"valid_upload_{i}.txt" for i in range(25)]

    # Generate 25 path traversal / malicious filenames
    base_malicious = [
        "../test.txt",
        "../../../etc/passwd",
        "/etc/shadow",
        "dir/../../file.txt",
        "/absolute/path.png",
        "....//multiple_dots.txt",
        "some_dir/../another_dir/../target",
        "/var/run/secrets",
        "../"
    ]
    malicious_files = (base_malicious * 3)[:25]

    correct_responses = 0
    total_requests = 50

    # Ensure upload directory exists for the C program to write to
    os.makedirs("/tmp/uploads", exist_ok=True)

    # Test benign requests (Expected to succeed / return 0)
    for fname in benign_files:
        try:
            res = subprocess.run(
                [exe_path, expected_token, fname],
                input=b"dummy file content",
                capture_output=True,
                timeout=2
            )
            if res.returncode == 0:
                correct_responses += 1
        except subprocess.TimeoutExpired:
            pass # Treat timeout as failure

    # Test malicious requests (Expected to fail / return non-zero)
    for fname in malicious_files:
        try:
            res = subprocess.run(
                [exe_path, expected_token, fname],
                input=b"dummy file content",
                capture_output=True,
                timeout=2
            )
            # The patched program should reject path traversal (return non-zero)
            if res.returncode != 0:
                correct_responses += 1
        except subprocess.TimeoutExpired:
            pass # Treat timeout as failure

    # Calculate metric
    accuracy = correct_responses / total_requests

    # Assert against threshold
    assert accuracy == 1.0, (
        f"Security and functionality accuracy is {accuracy} (Threshold: 1.0). "
        f"Passed {correct_responses}/{total_requests} tests. "
        "Ensure the patch strictly rejects filenames containing '../' or starting with '/', "
        "and correctly validates the new SHA-256 token."
    )