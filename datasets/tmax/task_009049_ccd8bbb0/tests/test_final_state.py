# test_final_state.py

import os
import pytest

def test_extracted_valid_files():
    file1 = '/home/user/docs/new_feature.md'
    file2 = '/home/user/docs/subdir/nested.md'

    assert os.path.isfile(file1), f"Expected file {file1} to be extracted."
    with open(file1, 'r') as f:
        assert f.read() == "valid 1\n", f"Content of {file1} is incorrect."

    assert os.path.isfile(file2), f"Expected file {file2} to be extracted."
    with open(file2, 'r') as f:
        assert f.read() == "valid 2\n", f"Content of {file2} is incorrect."

def test_rejected_malicious_files():
    malicious1 = '/home/user/docs_backup/overwrite.md'
    malicious2 = '/etc/passwd_fake'

    assert not os.path.exists(malicious1), f"Malicious file {malicious1} should not have been extracted."
    assert not os.path.exists(malicious2), f"Malicious file {malicious2} should not have been extracted."

def test_extraction_log():
    log_file = '/home/user/extraction_log.txt'
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    expected_lines = [
        "EXTRACTED: /home/user/docs/new_feature.md\n",
        "EXTRACTED: /home/user/docs/subdir/nested.md\n",
        "REJECTED: ../docs_backup/overwrite.md\n",
        "REJECTED: /etc/passwd_fake\n"
    ]

    with open(log_file, 'r') as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, f"Log file content does not match expected sorted output. Got: {actual_lines}"