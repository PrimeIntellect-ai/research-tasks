# test_final_state.py
import os
import subprocess
import pytest

def test_fuzzing_results():
    crash_log = "/home/user/crashes.log"
    binary = "/app/router_engine_stripped"
    ci_config = "/home/user/.github/workflows/fuzz.yml"

    assert os.path.exists(crash_log), f"{crash_log} not found. The fuzzer must create this file."
    assert os.path.exists(ci_config), f"CI config not found at {ci_config}."

    valid_crashes = 0
    with open(crash_log, "r") as f:
        urls = f.read().splitlines()

    # Test the discovered crashing URLs against the binary
    for url in set(urls):
        try:
            proc = subprocess.run([binary, url], capture_output=True, timeout=1)
            # Check for typical crash signals (e.g., -11 for SIGSEGV) or large exit codes
            if proc.returncode < 0 or proc.returncode > 127: 
                valid_crashes += 1
        except subprocess.TimeoutExpired:
            pass

    assert valid_crashes >= 3, f"Found {valid_crashes} valid unique crashes, expected >= 3. Ensure the fuzzer explores edge cases like long parameters or missing keys."