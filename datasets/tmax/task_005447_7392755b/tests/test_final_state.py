# test_final_state.py

import os
import re
import hashlib
import subprocess
import pytest

def compute_expected(line: str) -> str:
    # Remove trailing newline for processing
    content = line.rstrip('\n')

    # Redact private keys
    content = re.sub(r'-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----', '[REDACTED_KEY]', content)

    # Redact XSS payloads
    content = re.sub(r'<script>.*?</script>', '[MALICIOUS_PAYLOAD]', content)

    # Compute SHA-256 hash
    h = hashlib.sha256(content.encode('utf-8')).hexdigest()

    # Return formatted string with newline
    return f"{content} | SHA256: {h}\n"

def run_redactor(input_data: str) -> str:
    binary_path = "/home/user/redactor"
    if not os.path.isfile(binary_path):
        pytest.fail(f"Binary {binary_path} does not exist.")

    try:
        result = subprocess.run(
            [binary_path],
            input=input_data.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        return result.stdout.decode('utf-8')
    except Exception as e:
        pytest.fail(f"Execution of {binary_path} failed: {e}")

def test_clean_corpus():
    clean_dir = "/app/corpora/clean"
    if not os.path.isdir(clean_dir):
        pytest.fail(f"Clean corpus directory {clean_dir} does not exist.")

    files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    if not files:
        pytest.fail(f"No files found in {clean_dir}.")

    failed_files = []

    for filename in files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            input_data = f.read()

        expected_output = compute_expected(input_data)
        actual_output = run_redactor(input_data)

        if actual_output != expected_output:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(files)} clean modified. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_dir = "/app/corpora/evil"
    if not os.path.isdir(evil_dir):
        pytest.fail(f"Evil corpus directory {evil_dir} does not exist.")

    files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    if not files:
        pytest.fail(f"No files found in {evil_dir}.")

    failed_files = []

    for filename in files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            input_data = f.read()

        expected_output = compute_expected(input_data)
        actual_output = run_redactor(input_data)

        if actual_output != expected_output:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(files)} evil bypassed. Offending files: {', '.join(failed_files)}")