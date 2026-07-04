# test_final_state.py

import os
import stat
import pytest

def test_processed_authbase_log():
    """Check that AuthBase.log contains the correct FATAL line."""
    log_path = '/home/user/processed/AuthBase.log'
    assert os.path.isfile(log_path), f"File {log_path} is missing."
    with open(log_path, 'r') as f:
        content = f.read().strip()
    expected = "2023-10-01 10:00:01 | AuthBase | FATAL | Keymaster disconnected"
    assert expected in content, f"Expected FATAL line missing in {log_path}."

def test_processed_dbcore_log():
    """Check that DB_Core.log contains the correct FATAL line."""
    log_path = '/home/user/processed/DB_Core.log'
    assert os.path.isfile(log_path), f"File {log_path} is missing."
    with open(log_path, 'r') as f:
        content = f.read().strip()
    expected = "2023-10-01 10:00:03 | DB_Core | FATAL | Table corruption detected"
    assert expected in content, f"Expected FATAL line missing in {log_path}."

def test_processed_network_log():
    """Check that Network.log contains the correct FATAL line."""
    log_path = '/home/user/processed/Network.log'
    assert os.path.isfile(log_path), f"File {log_path} is missing."
    with open(log_path, 'r') as f:
        content = f.read().strip()
    expected = "2023-10-01 10:00:04 | Network | FATAL | Socket bind failed"
    assert expected in content, f"Expected FATAL line missing in {log_path}."

def test_archived_files():
    """Check that the processed files were moved to the archive directory."""
    archive_dir = '/home/user/archive'
    assert os.path.isfile(os.path.join(archive_dir, 'batch1.log')), "batch1.log was not moved to archive."
    assert os.path.isfile(os.path.join(archive_dir, 'batch2.gz')), "batch2.gz was not moved to archive."

def test_filter_executable_exists():
    """Check that the compiled C++ filter exists and is executable."""
    filter_path = '/home/user/filter'
    assert os.path.isfile(filter_path), f"Compiled filter {filter_path} is missing."
    st = os.stat(filter_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Filter {filter_path} is not executable."

def test_watcher_script_exists_and_executable():
    """Check that the Bash watcher script exists and is executable."""
    script_path = '/home/user/watch.sh'
    assert os.path.isfile(script_path), f"Watcher script {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Watcher script {script_path} is not executable."