# test_final_state.py
import os
import pytest

def test_legit_txt_extracted_and_converted():
    legit_path = '/home/user/extracted/legit.txt'
    assert os.path.exists(legit_path), f"File {legit_path} is missing. It should have been extracted."

    with open(legit_path, 'rb') as f:
        content = f.read()

    expected_content = "Café".encode('utf-8')
    assert content == expected_content, f"Content of {legit_path} is incorrect. Expected UTF-8 'Café', got {content}."

def test_zip_slip_prevented():
    evil_path = '/home/user/evil.txt'
    assert not os.path.exists(evil_path), f"File {evil_path} exists! Zip slip vulnerability was not prevented."

def test_skipped_log():
    log_path = '/home/user/skipped.log'
    assert os.path.exists(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert '../evil.txt' in lines, f"Expected '../evil.txt' in {log_path}, but got {lines}."
    assert len(lines) == 1, f"Expected exactly 1 skipped file in {log_path}, but got {len(lines)}."

def test_incremental_extraction_old_file_not_overwritten():
    old_path = '/home/user/extracted/subdir/old.txt'
    assert os.path.exists(old_path), f"File {old_path} is missing."

    with open(old_path, 'r') as f:
        content = f.read()

    assert content == "Original Old", f"File {old_path} was overwritten incorrectly. Expected 'Original Old', got '{content}'."

def test_incremental_extraction_new_file_overwritten():
    new_path = '/home/user/extracted/subdir/new.txt'
    assert os.path.exists(new_path), f"File {new_path} is missing."

    with open(new_path, 'r') as f:
        content = f.read()

    assert content == "Archive New", f"File {new_path} was not overwritten correctly. Expected 'Archive New', got '{content}'."

def test_lock_file_exists():
    lock_path = '/home/user/extracted/.extract.lock'
    assert os.path.exists(lock_path), f"Lock file {lock_path} is missing."

def test_script_exists():
    script_path = '/home/user/safe_extract.py'
    assert os.path.exists(script_path), f"Script {script_path} is missing."