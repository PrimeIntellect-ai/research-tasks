# test_final_state.py
import os
import subprocess
import pytest

AGENT_BINARY = "/home/user/rust_detector/target/release/detector"
CLEAN_CORPUS_DIR = "/app/eval/clean"
EVIL_CORPUS_DIR = "/app/eval/evil"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_BINARY), f"Agent binary not found at {AGENT_BINARY}"
    assert os.path.isfile(AGENT_BINARY), f"{AGENT_BINARY} is not a file"
    assert os.access(AGENT_BINARY, os.X_OK), f"Agent binary {AGENT_BINARY} is not executable"

def test_clean_corpus():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}"
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    assert len(clean_files) > 0, f"No CSV files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for csv_file in clean_files:
        result = subprocess.run([AGENT_BINARY, csv_file], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (should be accepted with exit code 0). "
                    f"Offending files: {', '.join(failed_files[:10])}{'...' if len(failed_files) > 10 else ''}")

def test_evil_corpus():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus directory missing: {EVIL_CORPUS_DIR}"
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    assert len(evil_files) > 0, f"No CSV files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for csv_file in evil_files:
        result = subprocess.run([AGENT_BINARY, csv_file], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (should be rejected with exit code 1). "
                    f"Offending files: {', '.join(failed_files[:10])}{'...' if len(failed_files) > 10 else ''}")