# test_final_state.py

import os
import zipfile
import pytest

def test_docs_safe_directory_contents():
    """Verify that only safe files were extracted to /home/user/docs_safe/."""
    safe_dir = '/home/user/docs_safe'
    assert os.path.isdir(safe_dir), f"Directory {safe_dir} does not exist."

    expected_files = {
        'intro.md',
        'guide/setup.md',
        'api_reference.md'
    }

    actual_files = set()
    for root, _, set_files in os.walk(safe_dir):
        for f in set_files:
            rel_path = os.path.relpath(os.path.join(root, f), safe_dir)
            actual_files.add(rel_path.replace('\\', '/'))

    assert expected_files.issubset(actual_files), f"Missing safe files: {expected_files - actual_files}"

    # Ensure no malicious files were extracted
    assert 'overwrite_sys.txt' not in actual_files, "Malicious file 'overwrite_sys.txt' was extracted!"
    assert 'shadow_fake' not in actual_files, "Malicious file 'shadow_fake' was extracted!"
    assert '../overwrite_sys.txt' not in actual_files, "Malicious file was extracted with path traversal!"

def test_safe_docs_bundle_exists_and_contents():
    """Verify that the safe_docs_bundle.zip exists and contains the correct files."""
    bundle_path = '/home/user/safe_docs_bundle.zip'
    assert os.path.isfile(bundle_path), f"Consolidated archive {bundle_path} does not exist."

    expected_files = {
        'intro.md',
        'guide/setup.md',
        'api_reference.md'
    }

    with zipfile.ZipFile(bundle_path, 'r') as z:
        actual_files = set(z.namelist())

        # Remove trailing slashes for directory entries if any
        actual_files = {f for f in actual_files if not f.endswith('/')}

    assert expected_files.issubset(actual_files), f"Bundle is missing safe files: {expected_files - actual_files}"
    assert 'overwrite_sys.txt' not in actual_files, "Bundle contains malicious file 'overwrite_sys.txt'"
    assert 'shadow_fake' not in actual_files, "Bundle contains malicious file 'shadow_fake'"

def test_malicious_zips_log():
    """Verify that the malicious zips log is correct and sorted."""
    log_path = '/home/user/malicious_zips.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        'doc_beta_malicious.zip',
        'doc_delta_bad.zip'
    ]

    assert lines == expected_lines, f"Log file contents are incorrect. Expected {expected_lines}, got {lines}."