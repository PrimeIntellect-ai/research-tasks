# test_final_state.py

import os
import pytest

def test_drop_directory_empty():
    """Verify that the drop directory is empty after processing."""
    drop_dir = '/home/user/storage_drop'
    assert os.path.exists(drop_dir), f"Directory {drop_dir} does not exist."
    assert os.path.isdir(drop_dir), f"{drop_dir} is not a directory."
    files = os.listdir(drop_dir)
    assert len(files) == 0, f"Drop directory is not empty. Found: {files}"

def test_processed_legacy_dump():
    """Verify that the first file was correctly processed, renamed, and encoded."""
    file_path = '/home/user/storage_archive/legacy_dump.txt.processed'
    assert os.path.exists(file_path), f"Processed file {file_path} does not exist."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    except UnicodeDecodeError:
        pytest.fail(f"File {file_path} is not valid UTF-8.")

    expected_content = 'Voilà, testing storage'
    assert content == expected_content, f"Content mismatch in {file_path}. Expected '{expected_content}', got '{content}'."

def test_processed_new_server_events():
    """Verify that the second file was correctly processed, renamed, and encoded."""
    file_path = '/home/user/storage_archive/new_server_events.log.processed'
    assert os.path.exists(file_path), f"Processed file {file_path} does not exist."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    except UnicodeDecodeError:
        pytest.fail(f"File {file_path} is not valid UTF-8.")

    expected_content = 'Café server crashed'
    assert content == expected_content, f"Content mismatch in {file_path}. Expected '{expected_content}', got '{content}'."

def test_final_state_log():
    """Verify that the final state log contains the names of the processed files."""
    log_file = '/home/user/final_state.log'
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."

    with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
        log_content = f.read()

    assert 'legacy_dump.txt.processed' in log_content, f"'legacy_dump.txt.processed' not found in {log_file}."
    assert 'new_server_events.log.processed' in log_content, f"'new_server_events.log.processed' not found in {log_file}."