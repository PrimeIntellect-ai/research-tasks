# test_final_state.py

import os
import re

def test_secret_params_recovered():
    secret_file = "/home/user/suspicious_repo/secret_params.h"
    assert os.path.isfile(secret_file), f"{secret_file} was not recovered."
    with open(secret_file, "r") as f:
        content = f.read()
    assert "0x8a9b2c3d" in content.lower() or "2325433405" in content, "The recovered secret_params.h does not contain the correct SECRET_MULTIPLIER."

def test_report_exists_and_valid():
    report_file = "/home/user/report.txt"
    assert os.path.isfile(report_file), f"Report file {report_file} does not exist."

    with open(report_file, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n") if line.strip()]

    assert len(lines) == 3, f"Report file must contain exactly 3 lines, found {len(lines)}."

    # Line 1: SECRET_MULTIPLIER
    multiplier_str = lines[0].lower()
    assert "0x8a9b2c3d" in multiplier_str or "2325433405" in multiplier_str, \
        f"Line 1 of report is incorrect. Expected SECRET_MULTIPLIER, got: {lines[0]}"

    # Line 2: Timestamp
    try:
        timestamp = int(lines[1])
    except ValueError:
        assert False, f"Line 2 must be a decimal integer, got: {lines[1]}"

    expected_multiplier = 2325433405
    modulo_result = (timestamp * expected_multiplier) % 99991
    assert modulo_result == 1337, \
        f"The timestamp {timestamp} does not cause the crash. (ts * MULTIPLIER) % 99991 = {modulo_result}, expected 1337."

    # Line 3: internal_hash
    hash_str = lines[2].lower()
    assert hash_str.startswith("0x"), f"Line 3 must be a hexadecimal value prefixed with '0x', got: {lines[2]}"

    try:
        internal_hash = int(hash_str, 16)
    except ValueError:
        assert False, f"Line 3 must be a valid hexadecimal integer, got: {lines[2]}"

    expected_hash = timestamp * expected_multiplier
    assert internal_hash == expected_hash, \
        f"Line 3 internal_hash is incorrect. Expected hex({expected_hash}), got {hash_str}."

def test_fuzzer_created():
    fuzzer_file = "/home/user/suspicious_repo/fuzzer.cpp"
    assert os.path.isfile(fuzzer_file), f"Fuzzer source file {fuzzer_file} was not created."