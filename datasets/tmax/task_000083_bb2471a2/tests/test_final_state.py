# test_final_state.py

import os
import subprocess
import pytest

def run_verify(path):
    cmd = [
        "cargo", "run", 
        "--manifest-path", "/home/user/backup_processor/Cargo.toml", 
        "--", "verify", path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def test_adversarial_corpus():
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus missing at {evil_dir}"

    clean_items = [d for d in os.listdir(clean_dir) if os.path.isdir(os.path.join(clean_dir, d))]
    evil_items = [d for d in os.listdir(evil_dir) if os.path.isdir(os.path.join(evil_dir, d))]

    clean_failed = []
    for item in clean_items:
        path = os.path.join(clean_dir, item)
        code, out, err = run_verify(path)
        if code != 0 or "ACCEPT" not in out:
            clean_failed.append(item)

    evil_failed = []
    for item in evil_items:
        path = os.path.join(evil_dir, item)
        code, out, err = run_verify(path)
        if code == 0 or "REJECT" not in out:
            evil_failed.append(item)

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_items)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_items)} evil bypassed: {', '.join(evil_failed)}")

    assert not errors, " | ".join(errors)