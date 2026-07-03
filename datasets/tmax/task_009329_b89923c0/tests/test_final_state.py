# test_final_state.py
import os
import tarfile
import pytest

def test_safe_extract_script_exists():
    assert os.path.isfile('/home/user/safe_extract.py'), "/home/user/safe_extract.py is missing"

def test_no_path_traversal_escape():
    # The malicious tar attempts to write to /tmp/escaped.txt
    # If safe_extract.py worked correctly, this file should not exist (or at least not be created by extraction)
    # We just check that it does not exist to ensure it didn't escape.
    assert not os.path.exists('/tmp/escaped.txt'), "Path traversal vulnerability exploited: /tmp/escaped.txt was created"

def test_app_complete_log():
    log_path = '/home/user/final_data/app_complete.log'
    assert os.path.isfile(log_path), f"{log_path} is missing"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "chunk1" in content, "app_complete.log does not contain 'chunk1'"
    assert "chunk2" in content, "app_complete.log does not contain 'chunk2'"
    assert "chunk3" in content, "app_complete.log does not contain 'chunk3'"

    # Ensure they are in alphabetical order
    idx1 = content.find("chunk1")
    idx2 = content.find("chunk2")
    idx3 = content.find("chunk3")
    assert idx1 < idx2 < idx3, "Log chunks are not in alphabetical order"

def test_bulk_renaming():
    csv1 = '/home/user/final_data/processed_metric_a1.csv'
    csv2 = '/home/user/final_data/processed_metric_b2.csv'

    assert os.path.isfile(csv1), f"{csv1} is missing"
    assert os.path.isfile(csv2), f"{csv2} is missing"

    # Check contents to ensure correct files were moved
    with open(csv1, 'r') as f:
        assert "1,2,3" in f.read(), f"Content of {csv1} is incorrect"

    with open(csv2, 'r') as f:
        assert "4,5,6" in f.read(), f"Content of {csv2} is incorrect"

def test_diff_backup_tar():
    tar_path = '/home/user/diff_backup.tar'
    assert os.path.isfile(tar_path), f"{tar_path} is missing"

    try:
        with tarfile.open(tar_path, 'r') as tar:
            names = tar.getnames()
    except tarfile.TarError:
        pytest.fail(f"{tar_path} is not a valid tar archive")

    # Check that the new/modified files are in the archive
    # The exact paths in the tar might vary (e.g. absolute vs relative), so we check basenames
    basenames = [os.path.basename(name) for name in names]

    assert "app_complete.log" in basenames, "app_complete.log is missing from diff_backup.tar"
    assert "processed_metric_a1.csv" in basenames, "processed_metric_a1.csv is missing from diff_backup.tar"
    assert "processed_metric_b2.csv" in basenames, "processed_metric_b2.csv is missing from diff_backup.tar"

    # Check that the old file from base_backup is NOT in the archive
    assert "processed_metric_old.csv" not in basenames, "processed_metric_old.csv should not be in the differential backup"