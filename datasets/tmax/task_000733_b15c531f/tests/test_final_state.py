# test_final_state.py
import os
import subprocess
import pytest
import glob

def test_rust_binary_exists():
    binary_path = '/home/user/alert_filter'
    assert os.path.isfile(binary_path), f"Rust binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Rust binary {binary_path} is not executable."

def test_adversarial_corpus_clean():
    binary_path = '/home/user/alert_filter'
    clean_dir = '/app/verifier/corpus/clean/'
    clean_files = glob.glob(os.path.join(clean_dir, '*'))

    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"

    failed_clean = []
    for f in clean_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(f))

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean files rejected (should be accepted): {failed_clean}"

def test_adversarial_corpus_evil():
    binary_path = '/home/user/alert_filter'
    evil_dir = '/app/verifier/corpus/evil/'
    evil_files = glob.glob(os.path.join(evil_dir, '*'))

    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"

    failed_evil = []
    for f in evil_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(f))

    assert not failed_evil, f"{len(failed_evil)} of {len(evil_files)} evil files bypassed (should be rejected): {failed_evil}"

def test_config_file_content():
    config_path = '/home/user/filter.toml'
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    with open(config_path, 'r') as f:
        content = f.read()

    assert "[filter]" in content, "Config file missing [filter] section."
    assert "strict_mode = true" in content.replace(" ", ""), "Config file missing strict_mode = true."

def test_config_file_acls():
    config_path = '/home/user/filter.toml'
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    # Check basic permissions for 'others'
    st = os.stat(config_path)
    assert (st.st_mode & 0o007) == 0, "Base permissions grant access to 'others' (should be o-rwx)."

    # Check ACLs
    result = subprocess.run(['getfacl', config_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl."

    acl_output = result.stdout
    assert "user:nobody:r--" in acl_output, "ACL for nobody does not grant read-only access (user:nobody:r--)."