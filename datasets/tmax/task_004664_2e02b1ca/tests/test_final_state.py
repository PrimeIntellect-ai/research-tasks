# test_final_state.py

import os
import subprocess
import pytest

SANITIZER_BIN = "/home/user/sanitizer"
CLEAN_CORPUS_DIR = "/var/test_corpus/clean"
EVIL_CORPUS_DIR = "/var/test_corpus/evil"

def test_sanitizer_binary_exists():
    assert os.path.exists(SANITIZER_BIN), f"Sanitizer binary not found at {SANITIZER_BIN}"
    assert os.path.isfile(SANITIZER_BIN), f"{SANITIZER_BIN} is not a file"
    assert os.access(SANITIZER_BIN, os.X_OK), f"Sanitizer binary {SANITIZER_BIN} is not executable"

def test_clean_corpus_accepted():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus missing at {CLEAN_CORPUS_DIR}"
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for fpath in clean_files:
        try:
            result = subprocess.run(
                [SANITIZER_BIN, fpath],
                capture_output=True,
                text=True,
                timeout=2
            )
            stdout = result.stdout.strip()
            if result.returncode != 0 or stdout != "CLEAN":
                failed_files.append((os.path.basename(fpath), result.returncode, stdout))
        except Exception as e:
            failed_files.append((os.path.basename(fpath), "ERROR", str(e)))

    if failed_files:
        details = "\n".join(f"{fname}: exit_code={code}, output={out}" for fname, code, out in failed_files)
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected:\n{details}")

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus missing at {EVIL_CORPUS_DIR}"
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for fpath in evil_files:
        try:
            result = subprocess.run(
                [SANITIZER_BIN, fpath],
                capture_output=True,
                text=True,
                timeout=2
            )
            stdout = result.stdout.strip()
            if result.returncode != 1 or stdout != "REJECT":
                failed_files.append((os.path.basename(fpath), result.returncode, stdout))
        except Exception as e:
            failed_files.append((os.path.basename(fpath), "ERROR", str(e)))

    if failed_files:
        details = "\n".join(f"{fname}: exit_code={code}, output={out}" for fname, code, out in failed_files)
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed:\n{details}")