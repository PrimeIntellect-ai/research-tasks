# test_final_state.py

import os
import subprocess
import stat
import pytest

SETUP_SCRIPT = "/home/user/setup_env.sh"
CLASSIFY_SCRIPT = "/home/user/classify_routes.sh"
MONITOR_STATE = "/home/user/monitor_state"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_setup_env_idempotent_and_correct():
    assert os.path.isfile(SETUP_SCRIPT), f"Setup script missing: {SETUP_SCRIPT}"

    # Run first time
    res1 = subprocess.run(["bash", SETUP_SCRIPT], capture_output=True, text=True)
    assert res1.returncode == 0, f"setup_env.sh failed on first run. stderr: {res1.stderr}"

    # Check directories and permissions
    for d in ["active", "archive", "quarantine"]:
        d_path = os.path.join(MONITOR_STATE, d)
        assert os.path.isdir(d_path), f"Directory {d_path} missing"
        mode = stat.S_IMODE(os.stat(d_path).st_mode)
        assert mode == 0o700, f"Directory {d_path} has incorrect permissions: {oct(mode)}, expected 0o700"

    # Check symlink
    link_path = os.path.join(MONITOR_STATE, "latest")
    assert os.path.islink(link_path), f"Symlink {link_path} missing"
    target = os.readlink(link_path)
    expected_targets = ["active", os.path.join(MONITOR_STATE, "active"), f"{MONITOR_STATE}/active"]
    assert target in expected_targets, f"Symlink target incorrect: {target}"

    # Run second time
    res2 = subprocess.run(["bash", SETUP_SCRIPT], capture_output=True, text=True)
    assert res2.returncode == 0, f"setup_env.sh failed on second run (not idempotent). stderr: {res2.stderr}"

    # Check symlink again
    assert os.path.islink(link_path), f"Symlink {link_path} missing after second run"
    target2 = os.readlink(link_path)
    assert target2 in expected_targets, f"Symlink target incorrect after second run: {target2}"

def test_classify_routes_adversarial():
    assert os.path.isfile(CLASSIFY_SCRIPT), f"Classify script missing: {CLASSIFY_SCRIPT}"

    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]

    assert len(clean_files) > 0, "Clean corpus is empty or missing"
    assert len(evil_files) > 0, "Evil corpus is empty or missing"

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run(["bash", CLASSIFY_SCRIPT, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        res = subprocess.run(["bash", CLASSIFY_SCRIPT, ef], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)