# test_final_state.py
import os
import glob
import subprocess
import pytest

def run_validator(filepath):
    # Run the go tool from the correct directory
    cmd = ["go", "run", "validator.go", filepath]
    try:
        result = subprocess.run(
            cmd,
            cwd="/app/backup-service",
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -1, str(e)

def test_clean_corpus():
    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    failed_files = []
    for filepath in clean_files:
        code, stdout = run_validator(filepath)
        if code != 0 or "ACCEPT" not in stdout:
            failed_files.append(os.path.basename(filepath))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_evil_corpus():
    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    bypassed_files = []
    for filepath in evil_files:
        code, stdout = run_validator(filepath)
        if code != 1 or "REJECT" not in stdout:
            bypassed_files.append(os.path.basename(filepath))

    assert len(bypassed_files) == 0, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"