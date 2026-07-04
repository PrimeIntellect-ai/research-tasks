# test_final_state.py

import os
import re
import time
import hashlib
import subprocess
import pytest

def test_sshd_config_hardened():
    config_path = "/home/user/sshd_config"
    assert os.path.isfile(config_path), f"File not found: {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # Check for 'no' values
    assert re.search(r"^\s*PermitRootLogin\s+no\b", content, re.MULTILINE), \
        "PermitRootLogin is not set to 'no' or is commented out."
    assert re.search(r"^\s*PasswordAuthentication\s+no\b", content, re.MULTILINE), \
        "PasswordAuthentication is not set to 'no' or is commented out."

    # Ensure no contradictory 'yes' values
    assert not re.search(r"^\s*PermitRootLogin\s+yes\b", content, re.MULTILINE), \
        "Found contradictory 'PermitRootLogin yes' in sshd_config."
    assert not re.search(r"^\s*PasswordAuthentication\s+yes\b", content, re.MULTILINE), \
        "Found contradictory 'PasswordAuthentication yes' in sshd_config."

def test_integrity_sha256():
    binary_path = "/home/user/redactor"
    hash_path = "/home/user/integrity.sha256"

    assert os.path.isfile(binary_path), f"Compiled binary not found: {binary_path}"
    assert os.path.isfile(hash_path), f"Checksum file not found: {hash_path}"

    # Calculate actual SHA256 of the binary
    sha256_hash = hashlib.sha256()
    with open(binary_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    actual_hash = sha256_hash.hexdigest()

    with open(hash_path, "r") as f:
        hash_content = f.read().strip()

    assert actual_hash in hash_content, \
        f"The SHA256 hash in {hash_path} does not match the actual hash of {binary_path}."

def test_redactor_performance_and_correctness(tmp_path):
    binary_path = "/home/user/redactor"
    assert os.path.isfile(binary_path), f"Compiled binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

    input_file = tmp_path / "hidden_test.log"
    output_file = tmp_path / "hidden_out.log"
    expected_file = tmp_path / "expected_hidden_out.log"

    # Generate a ~5MB test file (scaled down slightly for test stability, but enough to test performance)
    # The prompt mentions 50MB, so we'll generate a large enough file to be meaningful.
    # We'll generate 500,000 lines, which should be around 25-30MB.
    lines = []
    expected_lines = []

    test_cases = [
        ("User 1234-5678-9012-3456 logged in.", "User [REDACTED] logged in.\n"),
        ("Payment 1234 5678 9012 3456 processed.", "Payment [REDACTED] processed.\n"),
        ("Raw card 1234567890123456 found.", "Raw card [REDACTED] found.\n"),
        ("Normal log entry with numbers 1234 5678.", "Normal log entry with numbers 1234 5678.\n"),
        ("Short card 1234-5678-9012.", "Short card 1234-5678-9012.\n"),
    ]

    # Repeat to create a large file
    multiplier = 100000
    with open(input_file, "w") as fin, open(expected_file, "w") as fexp:
        for _ in range(multiplier):
            for raw, redacted in test_cases:
                fin.write(raw + "\n")
                fexp.write(redacted)

    # Run the redactor
    start_time = time.time()
    result = subprocess.run([binary_path, str(input_file), str(output_file)], capture_output=True, text=True)
    end_time = time.time()

    elapsed_time = end_time - start_time

    assert result.returncode == 0, f"Redactor failed with return code {result.returncode}\nStderr: {result.stderr}"
    assert os.path.isfile(output_file), "Redactor did not create the output file."

    # Verify correctness
    with open(output_file, "r") as fout, open(expected_file, "r") as fexp:
        # Check line by line to avoid loading massive files into memory
        for i, (out_line, exp_line) in enumerate(zip(fout, fexp)):
            assert out_line == exp_line, f"Mismatch at line {i+1}:\nExpected: {exp_line}\nGot: {out_line}"

    # Verify performance metric
    threshold = 0.5
    assert elapsed_time <= threshold, \
        f"Execution time metric failed: took {elapsed_time:.3f} seconds, which is > threshold of {threshold} seconds."