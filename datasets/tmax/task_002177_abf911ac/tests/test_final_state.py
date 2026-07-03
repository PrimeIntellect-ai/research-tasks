# test_final_state.py

import os
import subprocess
import pytest

def test_voicemail_code():
    """Test that the correct voicemail code was extracted."""
    code_file = "/home/user/voicemail_code.txt"
    assert os.path.exists(code_file), f"File {code_file} does not exist."
    with open(code_file, "r") as f:
        content = f.read().strip()
    assert content == "D925", f"Expected voicemail code 'D925', but got '{content}'."

def test_script_exists_and_executable():
    """Test that the validation script exists and is executable."""
    script_path = "/home/user/validate_filename.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_validate_filename_clean():
    """Test that the script accepts all clean filenames."""
    script_path = "/home/user/validate_filename.sh"
    clean_dir = "/app/corpora/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    clean_files = os.listdir(clean_dir)
    assert len(clean_files) > 0, "Clean corpus directory is empty."

    failed = []
    for filename in clean_files:
        res = subprocess.run([script_path, filename], capture_output=True)
        if res.returncode != 0:
            failed.append(filename)

    assert not failed, f"{len(failed)} of {len(clean_files)} clean filenames modified/rejected. Offending files: {failed}"

def test_validate_filename_evil():
    """Test that the script rejects all evil filenames."""
    script_path = "/home/user/validate_filename.sh"
    evil_dir = "/app/corpora/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    evil_files = os.listdir(evil_dir)
    assert len(evil_files) > 0, "Evil corpus directory is empty."

    failed = []
    for filename in evil_files:
        res = subprocess.run([script_path, filename], capture_output=True)
        if res.returncode == 0:
            failed.append(filename)

    assert not failed, f"{len(failed)} of {len(evil_files)} evil filenames bypassed/accepted. Offending files: {failed}"