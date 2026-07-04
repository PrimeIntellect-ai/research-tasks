# test_final_state.py
import os
import re
import subprocess
import pytest

def test_config_filter_exists_and_executable():
    binary_path = '/home/user/config_filter'
    assert os.path.isfile(binary_path), f"C binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"C binary at {binary_path} is not executable"

def test_config_filter_clean_corpus():
    binary_path = '/home/user/config_filter'
    clean_dir = '/app/corpus/clean'
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "Clean corpus directory is empty"

    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, 'rb') as f:
            original_content = f.read()

        result = subprocess.run([binary_path], input=original_content, capture_output=True)
        if result.returncode != 0 or result.stdout != original_content:
            modified_files.append(filename)

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean files modified. Offending files: {', '.join(modified_files)}"

def test_config_filter_evil_corpus():
    binary_path = '/home/user/config_filter'
    evil_dir = '/app/corpus/evil'
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "Evil corpus directory is empty"

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            original_text = f.read()

        expected_text = re.sub(r'AKIA[A-Z0-9]{16}', 'AKIA****************', original_text)

        with open(filepath, 'rb') as f:
            original_bytes = f.read()

        result = subprocess.run([binary_path], input=original_bytes, capture_output=True)

        try:
            output_text = result.stdout.decode('utf-8', errors='ignore')
        except Exception:
            output_text = ""

        if result.returncode != 0 or output_text != expected_text:
            bypassed_files.append(filename)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed. Offending files: {', '.join(bypassed_files)}"

def test_final_report():
    report_path = '/home/user/final_report.md'
    assert os.path.isfile(report_path), f"Final report not found at {report_path}"

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_content = """# Configuration Audit Report

## Service: auth-service
- Commit: 142
- Configuration: "{ "aws_key": "AKIA****************", "role": "admin" }"

## Service: auth-service
- Commit: 1024
- Configuration: "{ "token": "standard_token", "refresh": false }"

## Service: payment-gateway
- Commit: 512
- Configuration: "key=AKIA****************;mode=prod"
""".strip()

    assert content == expected_content, "Final report content does not match the expected output exactly."