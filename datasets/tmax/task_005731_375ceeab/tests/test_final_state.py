# test_final_state.py
import os
import re
import hashlib
import pytest

def get_last_successful_deployment(log_path):
    if not os.path.exists(log_path):
        return {}

    with open(log_path, 'r') as f:
        content = f.read()

    records = re.findall(r'\[DEPLOY_START\](.*?)\[DEPLOY_END\]', content, re.DOTALL)

    last_success_files = {}
    for record in records:
        if 'Status: SUCCESS' in record:
            last_success_files = {}
            lines = record.strip().split('\n')
            for line in lines:
                match = re.match(r'\s*-\s*(/\S+)\s*\(sha256:\s*([a-f0-9]+)\)', line)
                if match:
                    filepath, filehash = match.groups()
                    last_success_files[filepath] = filehash

    return last_success_files

def get_current_files(directory):
    current_files = {}
    if not os.path.exists(directory):
        return current_files

    for filename in os.listdir(directory):
        if filename.endswith('.yaml') or filename.endswith('.conf'):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    filehash = hashlib.sha256(f.read()).hexdigest()
                current_files[filepath] = filehash
    return current_files

def test_pending_changes_report():
    report_path = "/home/user/pending_changes.txt"
    assert os.path.isfile(report_path), f"The report file {report_path} was not found."

    log_path = "/home/user/deploy.log"
    config_dir = "/home/user/app_config"

    last_success = get_last_successful_deployment(log_path)
    current_files = get_current_files(config_dir)

    expected_lines = []

    # Check for NEW and MODIFIED
    for filepath, current_hash in current_files.items():
        if filepath not in last_success:
            expected_lines.append(f"NEW: {filepath} (sha256: {current_hash})")
        elif last_success[filepath] != current_hash:
            expected_lines.append(f"MODIFIED: {filepath} (sha256: {current_hash})")

    # Check for DELETED
    for filepath in last_success:
        if filepath not in current_files:
            expected_lines.append(f"DELETED: {filepath}")

    expected_lines.sort()
    expected_content = "\n".join(expected_lines) + "\n" if expected_lines else ""

    with open(report_path, 'r') as f:
        actual_content = f.read()

    # Standardize line endings for comparison
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines_clean = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines_clean, (
        f"The contents of {report_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines_clean)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )