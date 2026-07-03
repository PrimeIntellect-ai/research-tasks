# test_final_state.py
import os
import subprocess
import pytest

ENTRY_POINT = "/home/user/validate_batch"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def run_validator(batch_dir: str) -> str:
    """Run the user's validation script and return its stripped output."""
    try:
        result = subprocess.run(
            [ENTRY_POINT, batch_dir],
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_entry_point_exists_and_executable():
    assert os.path.isfile(ENTRY_POINT), f"Entry point {ENTRY_POINT} does not exist."
    assert os.access(ENTRY_POINT, os.X_OK), f"Entry point {ENTRY_POINT} is not executable."

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing."
    batches = [os.path.join(CLEAN_CORPUS_DIR, d) for d in os.listdir(CLEAN_CORPUS_DIR) if os.path.isdir(os.path.join(CLEAN_CORPUS_DIR, d))]
    assert len(batches) > 0, "No batches found in clean corpus."

    failures = []
    for batch in batches:
        output = run_validator(batch)
        if output != "ACCEPT":
            failures.append(f"{os.path.basename(batch)} (Output: {output})")

    assert not failures, f"{len(failures)} of {len(batches)} clean batches modified/rejected. Offending batches: {', '.join(failures)}"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing."
    batches = [os.path.join(EVIL_CORPUS_DIR, d) for d in os.listdir(EVIL_CORPUS_DIR) if os.path.isdir(os.path.join(EVIL_CORPUS_DIR, d))]
    assert len(batches) > 0, "No batches found in evil corpus."

    failures = []
    for batch in batches:
        output = run_validator(batch)
        if output != "REJECT":
            failures.append(f"{os.path.basename(batch)} (Output: {output})")

    assert not failures, f"{len(failures)} of {len(batches)} evil batches bypassed/accepted. Offending batches: {', '.join(failures)}"