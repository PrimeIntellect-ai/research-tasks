# test_final_state.py

import os
import stat
import subprocess
import glob
import pytest

def test_completion_log():
    log_path = "/home/user/app/completion.log"
    assert os.path.isfile(log_path), f"Missing completion log: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in completion log, found {len(lines)}"
    assert lines[0] == "/home/user/app/sanitizer.sh", f"Line 1 incorrect: {lines[0]}"
    assert lines[1] == "/home/user/app/ipc/v1/db.fifo", f"Line 2 incorrect: {lines[1]}"

def test_ipc_structure_and_permissions():
    v1_dir = "/home/user/app/ipc/v1"
    v2_dir = "/home/user/app/ipc/v2"

    assert os.path.isdir(v1_dir), f"Directory missing: {v1_dir}"
    assert os.path.isdir(v2_dir), f"Directory missing: {v2_dir}"

    v2_stat = os.stat(v2_dir)
    assert stat.S_IMODE(v2_stat.st_mode) == 0o700, f"Incorrect permissions on {v2_dir}, expected 0700"

    for fifo_name in ["backend.fifo", "db.fifo"]:
        v2_fifo = os.path.join(v2_dir, fifo_name)
        v1_symlink = os.path.join(v1_dir, fifo_name)

        assert os.path.exists(v2_fifo), f"FIFO missing: {v2_fifo}"
        assert stat.S_ISFIFO(os.stat(v2_fifo).st_mode), f"Not a FIFO: {v2_fifo}"
        assert stat.S_IMODE(os.stat(v2_fifo).st_mode) == 0o600, f"Incorrect permissions on {v2_fifo}, expected 0600"

        assert os.path.islink(v1_symlink), f"Symlink missing or not a link: {v1_symlink}"
        assert os.path.realpath(v1_symlink) == os.path.realpath(v2_fifo), f"Symlink {v1_symlink} does not point to {v2_fifo}"

def test_init_db_exp_exists():
    exp_path = "/home/user/app/init_db.exp"
    assert os.path.isfile(exp_path), f"Missing init_db.exp script: {exp_path}"

def test_sanitizer_adversarial_corpus():
    sanitizer = "/home/user/app/sanitizer.sh"
    assert os.path.isfile(sanitizer), f"Missing sanitizer script: {sanitizer}"

    evil_dir = "/home/user/corpus/evil"
    clean_dir = "/home/user/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.txt"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.txt"))

    assert len(evil_files) > 0, "No evil corpus files found"
    assert len(clean_files) > 0, "No clean corpus files found"

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run(["bash", sanitizer, f], capture_output=True, text=True)
        if "REJECT" not in res.stdout:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        res = subprocess.run(["bash", sanitizer, f], capture_output=True, text=True)
        if "ACCEPT" not in res.stdout:
            clean_modified.append(os.path.basename(f))

    assert not evil_bypassed, f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}"
    assert not clean_modified, f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}"