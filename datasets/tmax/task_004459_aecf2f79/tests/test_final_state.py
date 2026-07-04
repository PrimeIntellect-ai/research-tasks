# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_archive_permissions():
    archive_path = "/home/user/app/archive"
    assert os.path.isdir(archive_path), f"Archive directory missing: {archive_path}"

    st = os.stat(archive_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o700, f"Expected permissions 0o700 for {archive_path}, got {oct(permissions)}"

def test_cli_wrapper_exists():
    cli_path = "/home/user/app/worker/cli_test.js"
    assert os.path.isfile(cli_path), f"CLI wrapper missing: {cli_path}"

def test_adversarial_corpus():
    cli_path = "/home/user/app/worker/cli_test.js"
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    for fpath in clean_files:
        result = subprocess.run(["node", cli_path, fpath], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(fpath))

    evil_failed = []
    for fpath in evil_files:
        result = subprocess.run(["node", cli_path, fpath], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(fpath))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:5])}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed[:5])}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))