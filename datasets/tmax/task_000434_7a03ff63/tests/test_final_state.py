# test_final_state.py
import os
import subprocess

CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"
BINARY_PATH = "/home/user/config_sanitizer/target/release/config_sanitizer"
ORACLE_PATH = "/app/telemetry_oracle"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Expected Rust binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_clean_corpus():
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    assert clean_files, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        proc = subprocess.run([BINARY_PATH, f], capture_output=True)
        if proc.returncode != 0:
            failed_files.append(os.path.basename(f))
            continue

        oracle_proc = subprocess.run([ORACLE_PATH], input=proc.stdout, capture_output=True)
        if oracle_proc.returncode != 0:
            failed_files.append(os.path.basename(f))
            continue

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/failed. Offending files: {failed_files}"

def test_evil_corpus():
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    assert evil_files, "No evil corpus files found."

    bypassed_files = []
    for f in evil_files:
        proc = subprocess.run([BINARY_PATH, f], capture_output=True)
        if proc.returncode != 1:
            bypassed_files.append(os.path.basename(f))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {bypassed_files}"