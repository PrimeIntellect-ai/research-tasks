# test_final_state.py
import os
import subprocess
import concurrent.futures
import pytest

SCRIPT_PATH = "/home/user/detector.py"
LOG_PATH = "/home/user/scan_log.txt"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def run_detector(filepath):
    # Run the student's script using python3
    cmd = ["python3", SCRIPT_PATH, filepath]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return filepath, result.returncode, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return filepath, -1, "TIMEOUT"
    except Exception as e:
        return filepath, -1, str(e)

def test_detector_exists():
    assert os.path.exists(SCRIPT_PATH), f"Detector script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_adversarial_corpus_and_locking():
    # Ensure a fresh log file for the concurrent test
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    all_files = clean_files + evil_files
    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    results = []
    # Execute concurrently to test file locking requirements
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        futures = {executor.submit(run_detector, f): f for f in all_files}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    failed_clean = []
    failed_evil = []

    for filepath, retcode, stdout in results:
        if filepath in clean_files:
            if retcode != 0 or stdout != "ACCEPT":
                failed_clean.append((filepath, retcode, stdout))
        else:
            if retcode != 1 or stdout != "REJECT":
                failed_evil.append((filepath, retcode, stdout))

    error_msgs = []
    if failed_clean:
        examples = [os.path.basename(f[0]) for f in failed_clean[:5]]
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected. Examples: {examples}")
    if failed_evil:
        examples = [os.path.basename(f[0]) for f in failed_evil[:5]]
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted. Examples: {examples}")

    assert not error_msgs, " | ".join(error_msgs)

    # Check log file integrity (verifies proper locking)
    assert os.path.exists(LOG_PATH), f"Log file not created at {LOG_PATH}"
    with open(LOG_PATH, "r") as f:
        log_lines = f.read().splitlines()

    assert len(log_lines) == len(all_files), (
        f"Log file has {len(log_lines)} entries, expected {len(all_files)}. "
        "This indicates file locking failed during concurrent writes."
    )

    log_entries = set(log_lines)
    expected_entries = set()
    for f in clean_files:
        expected_entries.add(f"{f} ACCEPT")
    for f in evil_files:
        expected_entries.add(f"{f} REJECT")

    missing = expected_entries - log_entries
    extra = log_entries - expected_entries

    assert not missing and not extra, (
        "Log file contents do not match expected output exactly. "
        "Concurrent writes may have corrupted the lines (e.g., interleaved characters)."
    )