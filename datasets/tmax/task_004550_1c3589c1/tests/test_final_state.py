# test_final_state.py
import os
import pytest

def test_migrated_logs_content():
    raw_path = "/home/user/data/raw.csv"
    migrated_path = "/home/user/data/migrated_logs.csv"

    assert os.path.isfile(migrated_path), f"File {migrated_path} is missing. Did you run migrate.sh?"

    with open(raw_path, "r") as f:
        raw_lines = f.read().splitlines()

    expected_migrated = []
    for line in raw_lines:
        if not line.strip():
            continue
        parts = line.split(",")
        # original: timestamp,ip,endpoint,user_agent
        # new: timestamp,ip,method,endpoint
        expected_migrated.append(f"{parts[0]},{parts[1]},GET,{parts[2]}")

    with open(migrated_path, "r") as f:
        migrated_lines = f.read().splitlines()

    assert migrated_lines == expected_migrated, f"Content of {migrated_path} does not match expected schema migration."

def test_libvalidate_wrapper():
    lib_path = "/home/user/lib/libvalidate.sh"
    assert os.path.isfile(lib_path), f"File {lib_path} is missing."

    with open(lib_path, "r") as f:
        content = f.read()

    assert "validate_ip_v2" in content, "validate_ip_v2 function is missing in libvalidate.sh."
    assert "validate_ip" in content, "Original validate_ip function should not be removed."

def test_rate_limiter_exists():
    rl_path = "/home/user/app/rate_limiter.sh"
    assert os.path.isfile(rl_path), f"File {rl_path} is missing."
    assert os.access(rl_path, os.X_OK), f"File {rl_path} is not executable."

def test_final_processed_output():
    migrated_path = "/home/user/data/migrated_logs.csv"
    processed_path = "/home/user/output/final_processed.txt"
    errors_path = "/home/user/output/errors.log"

    assert os.path.isfile(processed_path), f"File {processed_path} is missing. Did you run processor.sh?"
    assert os.path.isfile(errors_path), f"File {errors_path} is missing."

    with open(migrated_path, "r") as f:
        migrated_lines = f.read().splitlines()

    expected_processed = []
    expected_errors = []

    import re
    ip_regex = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")

    counts = {}

    for line in migrated_lines:
        if not line.strip():
            continue
        ts, ip, method, endpoint = line.split(",")

        if not ip_regex.match(ip):
            expected_errors.append(f"INVALID IP: {ip}")
            continue

        key = (ip, ts)
        counts[key] = counts.get(key, 0) + 1

        if counts[key] > 2:
            expected_processed.append(f"{ts} {ip} {method} {endpoint} RATELIMITED")
        else:
            expected_processed.append(f"{ts} {ip} {method} {endpoint} ACCEPTED")

    with open(processed_path, "r") as f:
        processed_lines = f.read().splitlines()

    with open(errors_path, "r") as f:
        error_lines = f.read().splitlines()

    assert processed_lines == expected_processed, f"{processed_path} content does not match expected output based on rate limiting rules."
    assert error_lines == expected_errors, f"{errors_path} content does not match expected invalid IP errors."