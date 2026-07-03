# test_final_state.py

import os
import time
import subprocess

def test_fast_validator_exists_and_executable():
    rust_bin = "/home/user/fast_validator"
    assert os.path.exists(rust_bin), f"The fast_validator binary is missing at {rust_bin}."
    assert os.path.isfile(rust_bin), f"The path {rust_bin} is not a file."
    assert os.access(rust_bin, os.X_OK), f"The fast_validator binary at {rust_bin} is not executable."

def test_correctness():
    tokens_file = "/home/user/tokens.txt"
    valid_file = "/home/user/valid.txt"

    assert os.path.exists(valid_file), f"The output file {valid_file} is missing."

    expected_valid = []
    with open(tokens_file, 'r') as f:
        for line in f:
            token = line.strip()
            if not token:
                continue
            if token.startswith("SEC_"):
                xor_sum = 0
                for char in token:
                    xor_sum ^= ord(char)
                if xor_sum == 0x7F:
                    expected_valid.append(token)

    with open(valid_file, 'r') as f:
        actual_valid = [line.strip() for line in f if line.strip()]

    assert actual_valid == expected_valid, "The valid tokens produced do not match the expected valid tokens."

def test_speedup():
    tokens_file = "/home/user/tokens.txt"
    oracle = "/app/api_oracle"
    rust_bin = "/home/user/fast_validator"
    eval_output = "/home/user/valid_eval.txt"

    # Measure Oracle Baseline (subset of 1000 tokens to extrapolate)
    start_baseline = time.time()
    subprocess.run(f"head -n 1000 {tokens_file} | xargs -I {{}} {oracle} {{}}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    baseline_time_per_1k = time.time() - start_baseline
    estimated_baseline_total = baseline_time_per_1k * 1000 

    # Measure Agent Solution
    start_rust = time.time()
    subprocess.run(f"{rust_bin} {tokens_file} > {eval_output}", shell=True)
    rust_time = time.time() - start_rust

    speedup = estimated_baseline_total / rust_time
    assert speedup >= 50.0, f"Speedup {speedup:.2f}x is below the 50.0x threshold."

    # Verify eval output matches expected to ensure they didn't just write a no-op script
    expected_valid = []
    with open(tokens_file, 'r') as f:
        for line in f:
            token = line.strip()
            if not token:
                continue
            if token.startswith("SEC_"):
                xor_sum = 0
                for char in token:
                    xor_sum ^= ord(char)
                if xor_sum == 0x7F:
                    expected_valid.append(token)

    with open(eval_output, 'r') as f:
        actual_valid = [line.strip() for line in f if line.strip()]

    assert actual_valid == expected_valid, "The fast_validator did not produce the correct output during the speedup evaluation."