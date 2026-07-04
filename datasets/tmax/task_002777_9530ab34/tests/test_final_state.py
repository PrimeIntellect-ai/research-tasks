# test_final_state.py

import os
import json
import subprocess
import random
import time
import pytest

def test_audit_report_exists_and_format():
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON")

    assert "transcription" in report, "Missing 'transcription' key in audit report"
    assert "cwe_id" in report, "Missing 'cwe_id' key in audit report"
    assert "forged_pin" in report, "Missing 'forged_pin' key in audit report"

def test_audit_report_contents():
    report_path = "/home/user/audit_report.json"
    if not os.path.exists(report_path):
        pytest.skip("Audit report not found")

    with open(report_path, "r") as f:
        report = json.load(f)

    # Check transcription
    assert report["transcription"] == "7294", f"Incorrect transcription: {report['transcription']} (expected 7294)"

    # Check CWE ID
    cwe = report["cwe_id"].upper()
    assert cwe in ["CWE-121", "CWE-119"], f"Incorrect CWE ID: {cwe}. Expected CWE-121 or CWE-119"

def test_decrypt_tool_accuracy_and_performance():
    source_path = "/home/user/decrypt.c"
    bin_path = "/home/user/decrypt"

    assert os.path.exists(source_path), f"Source file not found at {source_path}"

    # Compile agent's code
    compile_res = subprocess.run(["gcc", "-O3", source_path, "-o", bin_path], capture_output=True)
    assert compile_res.returncode == 0, f"Compilation failed: {compile_res.stderr.decode()}"

    # C script to verify the hash directly using the target code
    verify_c = """
    #include <stdio.h>
    #include <stdint.h>
    #include <stdlib.h>
    uint64_t mix_hash(uint64_t input) {
        uint64_t state = input;
        for(int i = 0; i < 5; i++) {
            state ^= (state >> 12);
            state ^= (state << 25);
            state ^= (state >> 27);
        }
        return state;
    }
    int main(int argc, char** argv) {
        if (argc < 2) return 1;
        uint64_t val = strtoull(argv[1], NULL, 16);
        printf("0x%016lX\\n", mix_hash(val));
        return 0;
    }
    """
    verify_src = "/tmp/verify.c"
    verify_bin = "/tmp/verify_hash"

    with open(verify_src, "w") as f:
        f.write(verify_c)

    subprocess.run(["gcc", "-O3", verify_src, "-o", verify_bin], check=True)

    correct = 0
    num_tests = 10

    # Use a fixed seed for reproducibility in tests, or random
    random.seed(42)
    test_cases = [random.getrandbits(64) for _ in range(num_tests)]

    start_time = time.time()

    for target in test_cases:
        target_hex = f"0x{target:016X}"

        # Run agent's tool
        try:
            res = subprocess.run([bin_path, target_hex], capture_output=True, text=True, timeout=0.1)
            preimage_hex = res.stdout.strip()

            # Verify the preimage
            verify_res = subprocess.run([verify_bin, preimage_hex], capture_output=True, text=True, timeout=0.1)
            if verify_res.stdout.strip().upper() == target_hex.upper():
                correct += 1
        except subprocess.TimeoutExpired:
            pass

    elapsed = time.time() - start_time

    accuracy = correct / float(num_tests)
    assert accuracy >= 1.0, f"Accuracy {accuracy} failed to meet threshold 1.0"
    assert elapsed < 1.0, f"Execution time {elapsed:.2f}s exceeded 1.0s limit (likely brute-forcing)"

def test_forged_pin_in_report():
    report_path = "/home/user/audit_report.json"
    bin_path = "/home/user/decrypt"

    if not os.path.exists(report_path) or not os.path.exists(bin_path):
        pytest.skip("Prerequisites missing")

    with open(report_path, "r") as f:
        report = json.load(f)

    target_hash = "0x1337BEEFCAFE0000"

    # Use the verified decrypt tool to get the expected forged pin
    res = subprocess.run([bin_path, target_hash], capture_output=True, text=True)
    expected_pin = res.stdout.strip().upper()

    actual_pin = report["forged_pin"].strip().upper()
    assert actual_pin == expected_pin, f"Forged pin {actual_pin} does not match expected {expected_pin}"