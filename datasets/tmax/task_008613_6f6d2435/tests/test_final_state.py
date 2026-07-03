# test_final_state.py

import os
import pytest

def test_sanitize_script_exists():
    assert os.path.isfile('/home/user/sanitize.py'), "/home/user/sanitize.py does not exist."

def test_clean_logs_exist_and_named_correctly():
    clean_dir = '/home/user/logs/clean/'
    assert os.path.isdir(clean_dir), f"{clean_dir} directory is missing."

    expected_files = ['clean.log.000', 'clean.log.001', 'clean.log.002', 'clean.log.003']
    actual_files = sorted(os.listdir(clean_dir))

    for f in expected_files:
        assert f in actual_files, f"Expected file {f} is missing in {clean_dir}."

    # Optionally check if there are any extra files
    assert len(actual_files) == len(expected_files), f"Expected exactly {len(expected_files)} files in {clean_dir}, but found {len(actual_files)}: {actual_files}"

def test_clean_logs_line_counts():
    clean_dir = '/home/user/logs/clean/'

    expected_counts = {
        'clean.log.000': 1000,
        'clean.log.001': 1000,
        'clean.log.002': 1000,
        'clean.log.003': 467
    }

    total_lines = 0
    for filename, expected_count in expected_counts.items():
        filepath = os.path.join(clean_dir, filename)
        assert os.path.isfile(filepath), f"{filepath} is missing."
        with open(filepath, 'r') as f:
            lines = f.readlines()
            assert len(lines) == expected_count, f"Expected {expected_count} lines in {filename}, got {len(lines)}."
            total_lines += len(lines)

    assert total_lines == 3467, f"Expected total lines across all clean logs to be 3467, got {total_lines}."

def test_clean_logs_sanitization():
    clean_dir = '/home/user/logs/clean/'
    expected_files = ['clean.log.000', 'clean.log.001', 'clean.log.002', 'clean.log.003']

    redacted_found = False

    for filename in expected_files:
        filepath = os.path.join(clean_dir, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                assert "MALICIOUS_ENTRY" not in line, f"Found 'MALICIOUS_ENTRY' in {filename} at line {line_num}."
                assert "../" not in line, f"Found '../' in {filename} at line {line_num}."
                if "[REDACTED]" in line:
                    redacted_found = True

    assert redacted_found, "Expected to find '[REDACTED]' in the sanitized logs, but found none."